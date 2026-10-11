#!/usr/bin/env python3
"""Initialize, inspect, and run the sanitized Hermes starter runtime."""

from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hermes_lite.config import OPTIONAL_MODULES, RuntimePaths, initialize_runtime, load_config, module_settings, save_config  # noqa: E402
from hermes_lite.demo import seed_demo  # noqa: E402
from hermes_lite.ingest import create_ingest_server  # noqa: E402
from hermes_lite.providers import ProviderError, ProviderRouter  # noqa: E402
from hermes_lite.server import create_server  # noqa: E402
from hermes_lite.store import HermesStore  # noqa: E402


def runtime(args: argparse.Namespace) -> tuple[RuntimePaths, dict, HermesStore, ProviderRouter]:
    paths = RuntimePaths.from_root(args.root)
    config = load_config(paths)
    store = HermesStore(paths.database)
    router = ProviderRouter(config, paths.root)
    return paths, config, store, router


def command_init(args: argparse.Namespace) -> int:
    paths = RuntimePaths.from_root(args.root)
    created = initialize_runtime(paths, force=args.force)
    HermesStore(paths.database)
    print(f"Hermes runtime ready: {paths.root}")
    print(f"Configuration: {'created' if created else 'kept existing'}")
    print("Default provider: echo (offline, no credentials)")
    print("Next: python3 scripts/hermes.py doctor")
    return 0


def command_start(args: argparse.Namespace) -> int:
    """One explicit local setup; never replace existing configuration or data."""
    if args.demo and not args.root:
        args.root = str(REPO_ROOT / "private" / "Hermes_Demo")
    paths = RuntimePaths.from_root(args.root)
    try:
        initialize_runtime(paths)
        if args.demo:
            created = seed_demo(paths)
            print(f"Fictional sample workspace: {'created' if created else 'kept existing'}")
            print("Demo is offline-only and separate from the normal Hermes_Runtime directory.")
        else:
            from scripts.easy_setup import DEFAULT_TARGET, check_workspace, init_workspace
            target = paths.root / "AI_Knowledge_Base" if args.root else DEFAULT_TARGET
            result = check_workspace(target) if target.exists() else init_workspace(target, dry_run=False, force=False)
            if result:
                return result
        if command_doctor(args):
            return 1
        if args.setup_only:
            return 0
        return command_serve(args)
    except (ValueError, OSError) as exc:
        print(f"Could not start Hermes: {exc}", file=sys.stderr)
        return 2


def command_doctor(args: argparse.Namespace) -> int:
    paths, config, store, router = runtime(args)
    report = {
        "ok": True,
        "schema": config["schema"],
        "state_root": str(paths.root),
        "server": config.get("server", {}),
        "providers": router.status(),
        "modules": store.dashboard(module_settings(config)),
        "module_settings": module_settings(config),
    }
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("Hermes runtime: OK")
        print(f"Private state: {paths.root}")
        for name, status in report["providers"].items():
            print(f"Provider {name}: {status['reason']}")
        print("Core: nutrition, fitness (health)")
        for name in OPTIONAL_MODULES:
            print(f"Optional {name}: {'enabled' if module_settings(config)[name] else 'off'}")
    return 0


def command_serve(args: argparse.Namespace) -> int:
    _paths, config, store, router = runtime(args)
    server_config = config.get("server", {})
    host = args.host or server_config.get("host", "127.0.0.1")
    port = args.port if args.port is not None else int(server_config.get("port", 8765))
    if host not in {"127.0.0.1", "localhost", "::1"} and not args.allow_network:
        print("Refusing non-loopback binding without --allow-network.", file=sys.stderr)
        return 2
    server = create_server(store, router, host, port, demo_mode=bool(getattr(args, "demo", False)))
    actual_port = server.server_address[1]
    url = f"http://{host}:{actual_port}"
    print(f"Hermes dashboard: {url}")
    print("Press Ctrl-C to stop. No background service is installed.")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def command_chat(args: argparse.Namespace) -> int:
    _paths, _config, store, router = runtime(args)
    try:
        result = router.chat(args.message, args.provider)
    except (ValueError, ProviderError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if router.config.get("privacy", {}).get("log_chat_history", False):
        store.add_chat("cli", result["provider"], "user", args.message)
        store.add_chat("cli", result["provider"], "assistant", result["text"])
    print(result["text"])
    return 0


def command_health_ingest(args: argparse.Namespace) -> int:
    _paths, _config, store, _router = runtime(args)
    username = os.environ.get("HERMES_HEALTH_USERNAME", "hermes").strip()
    password = os.environ.get("HERMES_HEALTH_PASSWORD", "").strip()
    if not password:
        print("Set HERMES_HEALTH_PASSWORD before starting LAN ingest.", file=sys.stderr)
        return 2
    server = create_ingest_server(store, args.host, args.port, username, password)
    print(f"Hermes Health ingest: http://{args.host}:{server.server_address[1]}/health/import")
    print("Authentication: configured from environment; credentials are not printed or stored.")
    print("Press Ctrl-C to stop. Use a private LAN or authenticated HTTPS tunnel only.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def command_provider(args: argparse.Namespace) -> int:
    paths = RuntimePaths.from_root(args.root)
    config = load_config(paths)
    entries = config.get("providers", {}).get("entries", {})
    if args.name not in entries:
        print(f"Unknown provider: {args.name}", file=sys.stderr)
        return 2
    entries[args.name]["enabled"] = args.action == "enable"
    if args.default:
        if args.action != "enable":
            print("A disabled provider cannot be the default.", file=sys.stderr)
            return 2
        config["providers"]["default"] = args.name
    save_config(paths, config)
    print(f"Provider {args.name}: {args.action}d")
    if args.default:
        print(f"Default provider: {args.name}")
    print("No credential was read or written. Run doctor to check environment readiness.")
    return 0


def command_module(args: argparse.Namespace) -> int:
    paths = RuntimePaths.from_root(args.root)
    config = load_config(paths)
    config.setdefault("modules", {})[args.name] = {"enabled": args.action == "enable"}
    save_config(paths, config)
    print(f"{args.name.title()}: {'enabled' if args.action == 'enable' else 'off'}. Existing records kept.")
    print("Restart a running dashboard to load CLI changes, or use its Optional modules controls.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="owner-selected private runtime directory")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="initialize safely and start the localhost dashboard")
    start.add_argument("--demo", action="store_true", help="use a separate, offline fictional sample workspace")
    start.add_argument("--open", action="store_true", help="open the dashboard in your browser")
    start.add_argument("--port", type=int)
    start.add_argument("--setup-only", action="store_true", help="initialize and check without starting a server")
    start.set_defaults(func=command_start, host="127.0.0.1", allow_network=False)

    init = sub.add_parser("init", help="create private runtime config and database")
    init.add_argument("--force", action="store_true", help="replace private config only")
    init.set_defaults(func=command_init)

    doctor = sub.add_parser("doctor", help="show safe runtime readiness")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    serve = sub.add_parser("serve", help="run the local dashboard")
    serve.add_argument("--host")
    serve.add_argument("--port", type=int)
    serve.add_argument("--allow-network", action="store_true")
    serve.add_argument("--open", action="store_true")
    serve.set_defaults(func=command_serve)

    chat = sub.add_parser("chat", help="send one message through the provider router")
    chat.add_argument("message")
    chat.add_argument("--provider")
    chat.set_defaults(func=command_chat)

    ingest = sub.add_parser("health-ingest", help="run authenticated HealthKit LAN ingest")
    ingest.add_argument("--host", default="0.0.0.0")
    ingest.add_argument("--port", type=int, default=9121)
    ingest.set_defaults(func=command_health_ingest)

    provider = sub.add_parser("provider", help="enable or disable a private provider adapter")
    provider.add_argument("action", choices=["enable", "disable"])
    provider.add_argument("name", choices=["echo", "openai", "codex_cli", "ollama", "openai_compatible"])
    provider.add_argument("--default", action="store_true", help="also make the enabled provider the default")
    provider.set_defaults(func=command_provider)
    module = sub.add_parser("module", help="explicitly opt into or disable an optional local module")
    module.add_argument("action", choices=["enable", "disable"])
    module.add_argument("name", choices=OPTIONAL_MODULES)
    module.set_defaults(func=command_module)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
