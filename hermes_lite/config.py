"""Configuration and private-path helpers for the public Hermes runtime."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_CONFIG = REPO_ROOT / "runtime.example.json"


@dataclass(frozen=True)
class RuntimePaths:
    root: Path
    config: Path
    database: Path

    @classmethod
    def from_root(cls, raw: str | Path | None = None) -> "RuntimePaths":
        selected = raw or os.environ.get("HERMES_PRIVATE_ROOT")
        root = (
            Path(selected).expanduser()
            if selected
            else REPO_ROOT / "private" / "Hermes_Runtime"
        ).resolve()
        return cls(root=root, config=root / "config.json", database=root / "hermes.sqlite3")


def example_config() -> dict[str, Any]:
    return json.loads(EXAMPLE_CONFIG.read_text(encoding="utf-8"))


def initialize_runtime(paths: RuntimePaths, *, force: bool = False) -> bool:
    """Create a private config without ever copying credentials into it."""
    paths.root.mkdir(parents=True, exist_ok=True)
    if paths.config.exists() and not force:
        return False
    paths.config.write_text(
        json.dumps(example_config(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return True


def load_config(paths: RuntimePaths) -> dict[str, Any]:
    if not paths.config.exists():
        initialize_runtime(paths)
    data = json.loads(paths.config.read_text(encoding="utf-8"))
    if data.get("schema") != "hermes.runtime.v1":
        raise ValueError("Unsupported Hermes runtime configuration schema")
    return data
