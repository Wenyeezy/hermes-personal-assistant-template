from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "easy_setup.py"
PRIVACY_SCRIPT = REPO_ROOT / "scripts" / "privacy_check.py"


class EasySetupTests(unittest.TestCase):
    def run_setup(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "knowledge"
            result = self.run_setup("init", "--target", str(target), "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(target.exists())

    def test_init_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "knowledge"
            init_result = self.run_setup("init", "--target", str(target))
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            state = json.loads(
                (target / ".easy-setup-state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["schema"], "hermes.easy-setup.v1")
            self.assertFalse(state["contains_credentials"])
            self.assertEqual(state["integrations_authorized"], [])
            check_result = self.run_setup("check", "--target", str(target))
            self.assertEqual(check_result.returncode, 0, check_result.stderr)
            self.assertIn("Private scaffold: OK", check_result.stdout)

    def test_existing_files_are_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "knowledge"
            target.mkdir()
            marker = target / "START_HERE.md"
            marker.write_text("owner content\n", encoding="utf-8")
            result = self.run_setup("init", "--target", str(target))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(marker.read_text(encoding="utf-8"), "owner content\n")

    def test_public_tree_privacy_check_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PRIVACY_SCRIPT)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
