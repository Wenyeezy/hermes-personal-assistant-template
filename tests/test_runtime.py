from __future__ import annotations

import json
import os
import base64
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from hermes_lite.config import RuntimePaths, initialize_runtime, load_config
from hermes_lite.ingest import create_ingest_server
from hermes_lite.providers import ProviderError, ProviderRouter
from hermes_lite.server import create_server
from hermes_lite.store import HermesStore


class RuntimeTests(unittest.TestCase):
    def test_runtime_initializes_private_config_and_database(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            self.assertTrue(initialize_runtime(paths))
            store = HermesStore(paths.database)
            self.assertTrue(paths.config.is_file())
            self.assertTrue(paths.database.is_file())
            self.assertEqual(store.dashboard()["career"], {})
            config = load_config(paths)
            self.assertEqual(config["providers"]["default"], "echo")

    def test_all_local_modules_accept_and_summarize_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = HermesStore(Path(temp_dir) / "data.sqlite3")
            store.add_nutrition({"description": "Example meal", "calories": 500, "protein_g": 30})
            store.add_health({"steps": 7500, "exercise_minutes": 35})
            store.add_finance({"description": "Example expense", "amount": 12.5})
            store.add_career({"company": "Example Co", "role": "Example Role"})
            dashboard = store.dashboard()
            self.assertEqual(dashboard["nutrition"]["entries"], 1)
            self.assertEqual(dashboard["health"]["steps"], 7500)
            self.assertEqual(dashboard["finance"]["needs_review"], 1)
            self.assertEqual(dashboard["career"]["saved"], 1)

    def test_enhanced_nutrition_goals_summary_and_healthkit_export(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = HermesStore(Path(temp_dir) / "data.sqlite3")
            store.set_nutrition_goals({"calories": 2200, "protein_g": 150, "fiber_g": 30})
            store.add_nutrition(
                {
                    "occurred_on": "2026-08-11",
                    "description": "Confirmed meal",
                    "calories": 600,
                    "protein_g": 40,
                    "fiber_g": 8,
                    "sodium_mg": 700,
                    "source": "label",
                }
            )
            store.add_nutrition(
                {
                    "occurred_on": "2026-08-11",
                    "description": "Unconfirmed estimate",
                    "calories": 999,
                    "status": "needs_review",
                }
            )
            summary = store.nutrition_summary("2026-08-11", "2026-08-11")
            self.assertEqual(summary["totals"]["calories"], 600)
            self.assertEqual(summary["totals"]["fiber_g"], 8)
            self.assertEqual(summary["goals"]["protein_g"], 150)
            exported = store.nutrition_health_export("2026-08-11")
            identifiers = {item["healthkit_identifier"] for item in exported["samples"]}
            self.assertIn("dietaryEnergyConsumed", identifiers)
            self.assertIn("dietaryFiber", identifiers)

    def test_router_defaults_to_offline_echo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            router = ProviderRouter(load_config(paths), paths.root)
            result = router.chat("hello")
            self.assertEqual(result["provider"], "echo")
            self.assertIn("local starter", result["text"])

    def test_sensitive_text_is_not_sent_to_cloud(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            config = load_config(paths)
            config["providers"]["entries"]["openai"]["enabled"] = True
            router = ProviderRouter(config, paths.root)
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-value"}):
                with self.assertRaisesRegex(ProviderError, "not sent"):
                    router.chat("My password is private", "openai")

    def test_named_routes_select_friend_configured_adapters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            config = load_config(paths)
            config["providers"]["entries"]["codex_cli"]["enabled"] = True
            router = ProviderRouter(config, paths.root)
            with mock.patch.object(router, "_codex_cli", return_value="cli answer"):
                result = router.chat("/gpt hello", "echo")
            self.assertEqual(result["provider"], "codex_cli")
            self.assertEqual(result["route"], "/gpt")
            self.assertEqual(result["text"], "cli answer")

    def test_openai_adapter_uses_responses_shape_without_storing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            config = load_config(paths)
            config["providers"]["entries"]["openai"]["enabled"] = True
            router = ProviderRouter(config, paths.root)
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-value"}):
                with mock.patch(
                    "hermes_lite.providers._json_request",
                    return_value={"output_text": "provider answer"},
                ) as request:
                    result = router.chat("ordinary hello", "openai")
            self.assertEqual(result["text"], "provider answer")
            payload = request.call_args.args[1]
            self.assertFalse(payload["store"])
            self.assertEqual(payload["input"], "ordinary hello")

    def test_food_photo_estimate_is_review_only_and_not_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            config = load_config(paths)
            config["providers"]["entries"]["openai"]["enabled"] = True
            router = ProviderRouter(config, paths.root)
            provider_payload = {
                "description": "Example bowl",
                "calories": 520,
                "protein_g": 32,
                "carbs_g": 60,
                "fat_g": 18,
                "fiber_g": 9,
                "sugar_g": 7,
                "sodium_mg": 640,
                "confidence": 0.72,
                "notes": "Portion size is uncertain.",
            }
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-value"}):
                with mock.patch(
                    "hermes_lite.providers._json_request",
                    return_value={"output_text": json.dumps(provider_payload)},
                ) as request:
                    estimate = router.estimate_nutrition("data:image/png;base64,YWJj")
            self.assertEqual(estimate["status"], "needs_review")
            self.assertEqual(estimate["source"], "provider_estimate")
            self.assertEqual(estimate["calories"], 520)
            self.assertFalse(request.call_args.args[1]["store"])
            store = HermesStore(paths.database)
            self.assertEqual(store.recent("nutrition"), [])

    def test_http_dashboard_and_module_api(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = RuntimePaths.from_root(temp_dir)
            initialize_runtime(paths)
            config = load_config(paths)
            store = HermesStore(paths.database)
            router = ProviderRouter(config, paths.root)
            server = create_server(store, router, "127.0.0.1", 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with urllib.request.urlopen(base + "/") as response:
                    self.assertIn(b"Hermes Local Starter", response.read())
                request = urllib.request.Request(
                    base + "/api/nutrition",
                    data=json.dumps({"description": "Test meal", "calories": 420}).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request) as response:
                    self.assertEqual(response.status, 201)
                with urllib.request.urlopen(base + "/api/status") as response:
                    status = json.loads(response.read())
                self.assertEqual(status["modules"]["nutrition"]["entries"], 1)
                with self.assertRaises(urllib.error.HTTPError) as invalid_limit:
                    urllib.request.urlopen(base + "/api/nutrition?limit=not-a-number")
                self.assertEqual(invalid_limit.exception.code, 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_authenticated_healthkit_ingest_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = HermesStore(Path(temp_dir) / "data.sqlite3")
            server = create_ingest_server(store, "127.0.0.1", 0, "friend", "test-password")
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_address[1]}"
            payload = {
                "source": "apple_health_bridge",
                "daily": {
                    "date": "2026-08-11",
                    "steps": 9876,
                    "exercise_min": 42,
                    "standing_minutes": 600,
                    "distance_km": 7.4,
                },
                "workouts": [
                    {
                        "activity": "walking",
                        "event_time": "2026-08-11T09:00:00Z",
                        "duration_min": 35,
                        "source_id": "healthkit-workout-1",
                    }
                ],
            }
            try:
                unauthenticated = urllib.request.Request(
                    base_url + "/health/import",
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(urllib.error.HTTPError) as unauthorized:
                    urllib.request.urlopen(unauthenticated)
                self.assertEqual(unauthorized.exception.code, 401)

                credential = base64.b64encode(b"friend:test-password").decode()
                authenticated = urllib.request.Request(
                    base_url + "/health/import",
                    data=json.dumps(payload).encode(),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Basic {credential}",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(authenticated) as response:
                    self.assertEqual(response.status, 200)
                status_request = urllib.request.Request(
                    base_url + "/health/status?date=2026-08-11",
                    headers={"Authorization": f"Basic {credential}"},
                )
                with urllib.request.urlopen(status_request) as response:
                    status = json.loads(response.read())
                self.assertEqual(status["latest"]["date"], "2026-08-11")
                self.assertEqual(status["latest"]["workouts_count"], 1)
                self.assertEqual(store.dashboard()["health"]["steps"], 9876)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_dashboard_uses_local_calendar_date(self) -> None:
        script = (REPO_ROOT / "hermes_lite" / "static" / "app.js").read_text()
        self.assertIn("getFullYear()", script)
        self.assertIn("getMonth()", script)
        self.assertIn("getDate()", script)
        self.assertNotIn("toISOString().slice(0, 10)", script)
        self.assertIn('$$(".status-line", form).at(-1)', script)

    def test_cli_init_and_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            command = [sys.executable, str(REPO_ROOT / "scripts" / "hermes.py"), "--root", temp_dir]
            init = subprocess.run(command + ["init"], text=True, capture_output=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            doctor = subprocess.run(command + ["doctor", "--json"], text=True, capture_output=True)
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            report = json.loads(doctor.stdout)
            self.assertTrue(report["ok"])
            self.assertIn("nutrition", report["modules"])

            enabled = subprocess.run(
                command + ["provider", "enable", "codex_cli", "--default"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(enabled.returncode, 0, enabled.stderr)
            config = json.loads((Path(temp_dir) / "config.json").read_text())
            self.assertEqual(config["providers"]["default"], "codex_cli")
            self.assertTrue(config["providers"]["entries"]["codex_cli"]["enabled"])


if __name__ == "__main__":
    unittest.main()
