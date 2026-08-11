"""Small localhost dashboard and JSON API for Hermes Lite."""

from __future__ import annotations

import json
import mimetypes
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .providers import ProviderError, ProviderRouter
from .store import HermesStore


STATIC_ROOT = Path(__file__).resolve().parent / "static"
MAX_BODY_BYTES = 8_000_000


class HermesHTTPServer(ThreadingHTTPServer):
    store: HermesStore
    router: ProviderRouter


class HermesHandler(BaseHTTPRequestHandler):
    server_version = "HermesLite/1"

    @property
    def app(self) -> HermesHTTPServer:
        return self.server  # type: ignore[return-value]

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _headers(self, content_type: str, length: int) -> None:
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'")

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self._headers(content_type, len(body))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _read_json(self) -> dict[str, Any]:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("invalid content length") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ValueError("request body is empty or too large")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("request body must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            self._json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "modules": self.app.store.dashboard(),
                    "providers": self.app.router.status(),
                },
            )
            return
        if parsed.path.startswith("/api/"):
            query = parse_qs(parsed.query)
            if parsed.path == "/api/nutrition/summary":
                today = date.today().isoformat()
                try:
                    result = self.app.store.nutrition_summary(
                        query.get("start", [today])[0], query.get("end", [today])[0]
                    )
                except ValueError as exc:
                    self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                    return
                self._json(HTTPStatus.OK, result)
                return
            if parsed.path == "/api/nutrition/export":
                try:
                    result = self.app.store.nutrition_health_export(
                        query.get("date", [""])[0]
                    )
                except ValueError as exc:
                    self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                    return
                self._json(HTTPStatus.OK, {"ok": True, "result": result})
                return
            if parsed.path == "/api/health/summary":
                try:
                    days = int(query.get("days", ["7"])[0])
                except ValueError:
                    self._json(HTTPStatus.BAD_REQUEST, {"error": "days must be an integer"})
                    return
                self._json(HTTPStatus.OK, self.app.store.health_summary(days))
                return
            if parsed.path == "/api/health/workouts":
                self._json(HTTPStatus.OK, {"items": self.app.store.recent("workouts", limit=20)})
                return
            module = parsed.path.removeprefix("/api/")
            if module in {"nutrition", "health", "finance", "career"}:
                try:
                    limit = int(query.get("limit", ["20"])[0])
                except ValueError:
                    self._json(HTTPStatus.BAD_REQUEST, {"error": "limit must be an integer"})
                    return
                self._json(HTTPStatus.OK, {"items": self.app.store.recent(module, limit=limit)})
                return
            self._json(HTTPStatus.NOT_FOUND, {"error": "unknown API route"})
            return
        self._serve_static(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
            if parsed.path == "/api/chat":
                session_id = str(payload.get("session_id") or "dashboard")[:80]
                message = str(payload.get("message") or "")
                requested = payload.get("provider")
                log_chat = self.app.router.config.get("privacy", {}).get("log_chat_history", False)
                if log_chat:
                    self.app.store.add_chat(session_id, str(requested or "default"), "user", message)
                result = self.app.router.chat(message, str(requested) if requested else None)
                if log_chat:
                    self.app.store.add_chat(session_id, result["provider"], "assistant", result["text"])
                self._json(HTTPStatus.OK, result)
                return
            if parsed.path == "/api/nutrition/analyze-photo":
                estimate = self.app.router.estimate_nutrition(
                    str(payload.get("image_data_url") or ""),
                    str(payload.get("note") or ""),
                )
                self._json(HTTPStatus.OK, {"estimate": estimate, "persisted": False})
                return
            routes = {
                "/api/nutrition": self.app.store.add_nutrition,
                "/api/health": self.app.store.add_health,
                "/api/health/import": self.app.store.import_health,
                "/api/health/workouts": self.app.store.add_workout,
                "/api/nutrition/goals": self.app.store.set_nutrition_goals,
                "/api/finance": self.app.store.add_finance,
                "/api/career": self.app.store.add_career,
            }
            if parsed.path not in routes:
                self._json(HTTPStatus.NOT_FOUND, {"error": "unknown API route"})
                return
            item = routes[parsed.path](payload)
            self._json(HTTPStatus.CREATED, {"item": item})
        except (ValueError, ProviderError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "internal runtime error"})

    def _serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        candidate = (STATIC_ROOT / relative).resolve()
        try:
            candidate.relative_to(STATIC_ROOT.resolve())
        except ValueError:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if not candidate.is_file():
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"
        self._send_bytes(HTTPStatus.OK, body, content_type)


def create_server(
    store: HermesStore,
    router: ProviderRouter,
    host: str,
    port: int,
) -> HermesHTTPServer:
    server = HermesHTTPServer((host, port), HermesHandler)
    server.store = store
    server.router = router
    return server
