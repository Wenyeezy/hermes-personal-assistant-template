from __future__ import annotations
import json
import subprocess
import sys
import tarfile
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from hermes_lite.config import RuntimePaths, initialize_runtime, load_config
from hermes_lite.demo import seed_demo
from hermes_lite.providers import ProviderRouter
from hermes_lite.server import create_server
from hermes_lite.store import HermesStore
from scripts.build_preview import build, PUBLIC_FILES

class PreviewTests(unittest.TestCase):
    def test_demo_is_offline_separate_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = RuntimePaths.from_root(temp); initialize_runtime(paths)
            self.assertTrue(seed_demo(paths)); self.assertFalse(seed_demo(paths))
            store = HermesStore(paths.database)
            self.assertEqual(len(store.recent("nutrition")), 2)
            today = date.today().isoformat()
            self.assertEqual(store.nutrition_summary(today, today)["totals"]["calories"], 420)
            config = load_config(paths); config["providers"]["entries"]["openai"]["enabled"] = True
            paths.config.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError, "offline-only"): seed_demo(paths)

    def test_demo_refuses_existing_real_records(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = RuntimePaths.from_root(temp); initialize_runtime(paths)
            store = HermesStore(paths.database); store.add_career({"company":"Existing", "role":"Existing"})
            with self.assertRaisesRegex(ValueError, "existing records"): seed_demo(paths)
            self.assertEqual(len(store.recent("career")), 1)
            self.assertFalse((paths.root / ".fictional-demo.json").exists())

    def test_one_command_start_and_repeat_preserve_state(self):
        with tempfile.TemporaryDirectory() as temp:
            command = [sys.executable, str(REPO_ROOT / "scripts/hermes.py"), "--root", temp, "start", "--demo", "--setup-only"]
            for _ in range(2):
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            store = HermesStore(RuntimePaths.from_root(temp).database)
            self.assertEqual(len(store.recent("nutrition")), 2)

    def test_demo_refuses_goals_or_chat_only_workspaces(self):
        for existing in ("goals", "chat"):
            with tempfile.TemporaryDirectory() as temp:
                paths=RuntimePaths.from_root(temp); initialize_runtime(paths)
                store=HermesStore(paths.database)
                if existing == "goals": store.set_nutrition_goals({"calories":2000})
                else: store.add_chat("test", "echo", "user", "existing local record")
                with self.assertRaisesRegex(ValueError, "existing records"): seed_demo(paths)
                self.assertEqual(store.recent("nutrition"), [])

    def test_demo_rejects_untrusted_or_invalid_marker(self):
        with tempfile.TemporaryDirectory() as temp:
            paths=RuntimePaths.from_root(temp); initialize_runtime(paths)
            marker=paths.root/".fictional-demo.json"
            for value in ([], {"schema":"hermes.fictional-demo.v1","fictional":False}):
                marker.write_text(json.dumps(value))
                with self.assertRaisesRegex(ValueError, "Unknown demo marker"): seed_demo(paths)

    def test_static_bundle_allowlist_deterministic_and_symlink_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/"site"; source.mkdir()
            for name in PUBLIC_FILES: (source/name).write_text("fictional example")
            (source/"private.sqlite3").write_bytes(b"private"); (source/".env").write_text("SECRET=not-public")
            bundle=build(source,root/"dist","test"); first=bundle.read_bytes()
            self.assertEqual(build(source,root/"dist","test").read_bytes(), first)
            with tarfile.open(bundle) as archive: self.assertEqual(set(archive.getnames()), set(PUBLIC_FILES)|{"manifest.json"})
            (source/"index.html").unlink(); (source/"index.html").symlink_to(source/".env")
            with self.assertRaisesRegex(ValueError,"symlink"): build(source,root/"dist","test")
            with self.assertRaises(ValueError): build(source,root/"dist","../private")

    def test_loopback_host_origin_and_content_type_guards(self):
        with tempfile.TemporaryDirectory() as temp:
            paths=RuntimePaths.from_root(temp); initialize_runtime(paths)
            store=HermesStore(paths.database)
            server=create_server(store,ProviderRouter(load_config(paths),paths.root),"127.0.0.1",0,demo_mode=True)
            thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
            base=f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with urllib.request.urlopen(base+"/api/status") as response: self.assertTrue(json.loads(response.read())["demo_mode"])
                cases=[({"Host":"evil.example","Content-Type":"application/json"},403),({"Host":"[","Content-Type":"application/json"},400),({"Origin":"https://evil.example","Content-Type":"application/json"},403),({"Content-Type":"text/plain"},415)]
                for headers, code in cases:
                    request=urllib.request.Request(base+"/api/nutrition",data=b'{"description":"blocked"}',headers=headers)
                    with self.assertRaises(urllib.error.HTTPError) as error: urllib.request.urlopen(request)
                    self.assertEqual(error.exception.code,code)
                self.assertEqual(store.recent("nutrition"),[])
                request=urllib.request.Request(base+"/api/nutrition",data=b'{"description":"allowed"}',headers={"Origin":base,"Content-Type":"application/json"})
                with urllib.request.urlopen(request) as response: self.assertEqual(response.status,201)
            finally: server.shutdown(); server.server_close(); thread.join(timeout=2)

if __name__ == "__main__": unittest.main()
