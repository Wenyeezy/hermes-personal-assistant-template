"""Authenticated HealthKit-compatible ingest service for a fork owner's LAN."""

from __future__ import annotations

import base64
import hmac
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from .server import MAX_BODY_BYTES
from .store import HermesStore


class HealthIngestServer(ThreadingHTTPServer):
    store: HermesStore
    username: str
    password: str


class HealthIngestHandler(BaseHTTPRequestHandler):
    server_version = "HermesHealthIngest/1"

    @property
    def app(self) -> HealthIngestServer:
        return self.server  # type: ignore[return-value]

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if status == HTTPStatus.UNAUTHORIZED:
            self.send_header("WWW-Authenticate", 'Basic realm="Hermes Health Ingest"')
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(header[6:], validate=True).decode()
            username, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            return False
        return hmac.compare_digest(username, self.app.username) and hmac.compare_digest(
            password, self.app.password
        )

    def _require_auth(self) -> bool:
        if self._authorized():
            return True
        self._json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "unauthorized"})
        return False

    def _payload(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("invalid content length") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ValueError("request body is empty or too large")
        try:
            payload = json.loads(self.rfile.read(length).decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("request body must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/healthz":
            self._json(HTTPStatus.OK, {"ok": True, "service": "hermes-health-ingest"})
            return
        if not self._require_auth():
            return
        if parsed.path == "/health/authz":
            self._json(
                HTTPStatus.OK,
                {"ok": True, "service": "hermes-health-ingest", "auth": "ok"},
            )
            return
        query = parse_qs(parsed.query)
        if parsed.path == "/health/status":
            requested = query.get("date", [""])[0]
            result = self.app.store.health_summary(90)
            days = result["days"]
            latest = next(
                (item for item in days if not requested or item["occurred_on"] == requested),
                None,
            )
            workouts = [
                item
                for item in result["workouts"]
                if latest and item["occurred_on"] == latest["occurred_on"]
            ]
            self._json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "service": "hermes-health-ingest",
                    "target_date": requested or None,
                    "latest": None
                    if not latest
                    else {
                        "id": latest["occurred_on"],
                        "date": latest["occurred_on"],
                        "received_at": latest["created_at"],
                        "status": "local",
                        "source": latest["source"],
                        "workouts_count": len(workouts),
                        "has_activity_metrics": any(
                            latest.get(key) is not None
                            for key in ("steps", "active_calories", "exercise_minutes")
                        ),
                    },
                    "stale": latest is None,
                    "stale_reason": "no_health_import" if latest is None else "",
                },
            )
            return
        if parsed.path == "/nutrition/export":
            try:
                result = self.app.store.nutrition_health_export(
                    query.get("date", [""])[0]
                )
            except ValueError as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
                return
            self._json(HTTPStatus.OK, {"ok": True, "result": result})
            return
        self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/health/import":
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})
            return
        if not self._require_auth():
            return
        try:
            result = self.app.store.import_health(self._payload())
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return
        self._json(HTTPStatus.OK, {"ok": True, "result": result})


def create_ingest_server(
    store: HermesStore,
    host: str,
    port: int,
    username: str,
    password: str,
) -> HealthIngestServer:
    if not username or not password:
        raise ValueError("health ingest username and password are required")
    server = HealthIngestServer((host, port), HealthIngestHandler)
    server.store = store
    server.username = username
    server.password = password
    return server
