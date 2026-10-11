from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hermes_lite.config import RuntimePaths, initialize_runtime, load_config, module_settings
from hermes_lite.providers import ProviderRouter
from hermes_lite.server import create_server
from hermes_lite.store import HermesStore


class FocusTests(unittest.TestCase):
    def test_old_configuration_also_requires_optional_opt_in(self):
        self.assertFalse(module_settings({})["finance"])
        self.assertFalse(module_settings({"modules": {"finance": {"enabled": "true"}}})["finance"])
        self.assertTrue(module_settings({"modules": {"finance": {"enabled": True}}})["finance"])

    def test_meal_confirmation_is_explicit_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            store = HermesStore(Path(temp) / "data.sqlite3")
            meal = store.add_nutrition({"description": "Fictional pending meal", "calories": 610, "status": "needs_review"})
            self.assertEqual(store.dashboard()["nutrition"]["calories"], 0)
            with self.assertRaisesRegex(ValueError, "Explicit confirmation"):
                store.confirm_nutrition({"id": meal["id"]})
            for _ in range(2):
                result = store.confirm_nutrition({"id": meal["id"], "confirmed": True})
                self.assertEqual(result["id"], meal["id"])
            self.assertEqual(store.dashboard()["nutrition"]["calories"], 610)
            self.assertEqual(len(store.recent("nutrition")), 1)

    def test_finance_gate_persists_and_preserves_records(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = RuntimePaths.from_root(temp)
            initialize_runtime(paths)
            store = HermesStore(paths.database)
            store.add_finance({"description": "Existing fictional record", "amount": 12})
            config = load_config(paths)
            server = create_server(store, ProviderRouter(config, paths.root), "127.0.0.1", 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_address[1]}"

            def request(path, payload=None):
                headers = {"Content-Type": "application/json", "Origin": base}
                req = urllib.request.Request(base + path, headers=headers, data=None if payload is None else json.dumps(payload).encode())
                with urllib.request.urlopen(req) as response:
                    return json.loads(response.read())

            try:
                status = request("/api/status")
                self.assertFalse(status["module_settings"]["finance"])
                self.assertIsNone(status["modules"]["finance"])
                self.assertIsNone(status["modules"]["career"])
                for path, payload in (("/api/finance", None), ("/api/finance", {"description": "Blocked", "amount": 4}), ("/api/career", None)):
                    with self.assertRaises(urllib.error.HTTPError) as error:
                        request(path, payload)
                    self.assertEqual(error.exception.code, 403)
                with self.assertRaises(urllib.error.HTTPError) as error:
                    request("/api/modules", {"module": "finance", "enabled": "true"})
                self.assertEqual(error.exception.code, 400)
                request("/api/modules", {"module": "finance", "enabled": True})
                self.assertTrue(load_config(paths)["modules"]["finance"]["enabled"])
                self.assertEqual(len(request("/api/finance")["items"]), 1)
                request("/api/finance", {"description": "New fictional record", "amount": 3})
                request("/api/modules", {"module": "finance", "enabled": False})
                self.assertFalse(load_config(paths)["modules"]["finance"]["enabled"])
                self.assertEqual(len(store.recent("finance")), 2)
                self.assertEqual(load_config(paths)["providers"], config["providers"])
                self.assertFalse(load_config(paths)["privacy"]["log_chat_history"])
                request("/api/nutrition", {"description": "Meal without GPT", "calories": 420})
                request("/api/health/workouts", {"activity": "walking", "duration_minutes": 30})
                status = request("/api/status")
                self.assertEqual(status["modules"]["workout"]["minutes"], 30)
                self.assertEqual(status["modules"]["nutrition"]["calories"], 420)
            finally:
                server.shutdown(); server.server_close(); thread.join(timeout=2)

    def test_cli_optional_module_control(self):
        with tempfile.TemporaryDirectory() as temp:
            command = [sys.executable, str(ROOT / "scripts/hermes.py"), "--root", temp]
            for action, enabled in (("enable", True), ("disable", False)):
                result = subprocess.run(command + ["module", action, "finance"], text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(load_config(RuntimePaths.from_root(temp))["modules"]["finance"]["enabled"], enabled)

    def test_distinct_manual_workouts_save_and_imports_still_deduplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            store = HermesStore(Path(temp) / "data.sqlite3")
            for duration in (30, 15):
                store.add_workout({"activity": "Fictional walk", "duration_minutes": duration})
            self.assertEqual(store.dashboard()["workout"]["minutes"], 45)
            for _ in range(2):
                store.add_workout({"activity": "Imported sample", "duration_minutes": 10, "source_id": "sample-id"}, source="test-import")
            self.assertEqual(len(store.recent("workouts")), 3)

    def test_dashboard_does_not_query_disabled_optional_tables(self):
        with tempfile.TemporaryDirectory() as temp:
            store = HermesStore(Path(temp) / "data.sqlite3")
            with store.connect() as db:
                db.execute("DROP TABLE finance_entries")
                db.execute("DROP TABLE career_opportunities")
            dashboard = store.dashboard(module_settings({}))
            self.assertIsNone(dashboard["finance"])
            self.assertIsNone(dashboard["career"])


if __name__ == "__main__":
    unittest.main()
