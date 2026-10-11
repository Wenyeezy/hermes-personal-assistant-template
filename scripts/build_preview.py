#!/usr/bin/env python3
"""Package only the public fictional website; never package the repo root."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ("index.html", "styles.css", "media.css", "app.js", "fixtures.js", "icon.svg")
MEDIA_FILES = ("media/hermes-preview-wide.png", "media/hermes-preview-square.png", "media/hermes-preview-30s.mp4")


def build(source: Path, output: Path, version: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", version):
        raise ValueError("Use a short alphanumeric version without path separators.")
    if source.is_symlink():
        raise ValueError("The public source must not be a symlink.")
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    bundle = output / f"hermes-preview-{version}.tar.gz"
    selected: dict[str, bytes] = {}
    for name in PUBLIC_FILES + MEDIA_FILES:
        path = source / name
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError(f"Refusing symlink: {name}")
        if name in PUBLIC_FILES and not path.is_file():
            raise ValueError(f"Missing public file: {name}")
        if path.is_file():
            selected[name] = path.read_bytes()
    manifest = {"schema": "hermes.public-preview.v1", "version": version, "fictional_data_only": True,
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in selected.items()}}
    selected["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    # Fixed metadata prevents local paths, usernames and timestamps leaking into the archive.
    import io
    import gzip
    with bundle.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
        with tarfile.open(mode="w", fileobj=zipped) as archive:
            for name, data in sorted(selected.items()):
                info = tarfile.TarInfo(name); info.size = len(data); info.mode = 0o644; info.mtime = 0
                archive.addfile(info, io.BytesIO(data))
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.1.0-preview.1")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "dist")
    args = parser.parse_args()
    try:
        print(build(REPO_ROOT / "site", args.output, args.version))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Could not build public preview: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
