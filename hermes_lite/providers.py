"""Provider adapters and a conservative local-first router."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SENSITIVE = re.compile(
    r"\b(password|passcode|api[ _-]?key|secret|token|bank|account number|"
    r"social security|passport|medical|diagnosis)\b|密码|密钥|令牌|银行卡|"
    r"账号|身份证|护照|病历|诊断|精确地址",
    re.IGNORECASE,
)
CLOUD_PROVIDERS = {"openai", "codex_cli", "openai_compatible"}


class ProviderError(RuntimeError):
    pass


def _json_request(
    url: str,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ProviderError(f"Provider returned HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ProviderError("Provider is unreachable") from exc
    except json.JSONDecodeError as exc:
        raise ProviderError("Provider returned invalid JSON") from exc


def _responses_text(payload: dict[str, Any]) -> str:
    direct = payload.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    fragments: list[str] = []
    for item in payload.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str):
                    fragments.append(text)
    if not fragments:
        raise ProviderError("Provider response contained no output text")
    return "\n".join(fragments).strip()


class ProviderRouter:
    def __init__(self, config: dict[str, Any], state_root: str | Path):
        self.config = config
        self.state_root = Path(state_root)

    @property
    def entries(self) -> dict[str, dict[str, Any]]:
        return self.config.get("providers", {}).get("entries", {})

    def status(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for name, settings in self.entries.items():
            enabled = bool(settings.get("enabled"))
            ready = enabled
            reason = "ready" if ready else "disabled"
            if name == "openai" and enabled:
                ready = bool(os.environ.get(settings.get("api_key_env", "OPENAI_API_KEY")))
                reason = "ready" if ready else "missing API-key environment variable"
            elif name == "codex_cli" and enabled:
                ready = shutil.which("codex") is not None
                reason = "ready" if ready else "codex command not installed"
            elif name == "ollama" and enabled:
                model = os.environ.get(settings.get("model_env", "HERMES_OLLAMA_MODEL")) or settings.get("default_model")
                ready = bool(model)
                reason = "ready" if ready else "missing local model name"
            elif name == "openai_compatible" and enabled:
                base = os.environ.get(settings.get("base_url_env", "HERMES_COMPAT_BASE_URL"))
                model = os.environ.get(settings.get("model_env", "HERMES_COMPAT_MODEL"))
                ready = bool(base and model)
                reason = "ready" if ready else "missing compatible base URL or model"
            result[name] = {"enabled": enabled, "ready": ready, "reason": reason}
        return result

    def chat(self, message: str, provider: str | None = None) -> dict[str, Any]:
        clean_message = str(message or "").strip()
        if not clean_message:
            raise ValueError("message is required")
        provider_config = self.config.get("providers", {})
        routes = provider_config.get("routes", {})
        route_match = re.match(r"^/([a-zA-Z0-9_-]+)(?:\s+|$)", clean_message)
        routed_by = None
        if route_match and route_match.group(1) in routes:
            routed_by = "/" + route_match.group(1)
            selected = routes[route_match.group(1)]
            clean_message = clean_message[route_match.end() :].strip()
            if not clean_message:
                raise ValueError(f"Add a message after {routed_by}")
        else:
            selected = provider or provider_config.get("default", "echo")
        if selected not in self.entries:
            raise ProviderError(f"Unknown provider: {selected}")
        settings = self.entries[selected]
        if not settings.get("enabled"):
            raise ProviderError(f"Provider is disabled: {selected}")
        privacy = self.config.get("privacy", {})
        if (
            selected in CLOUD_PROVIDERS
            and SENSITIVE.search(clean_message)
            and not privacy.get("allow_sensitive_cloud", False)
        ):
            raise ProviderError(
                "Sensitive-looking content was not sent to a cloud provider. "
                "Use a configured local provider or explicitly change the private policy."
            )

        handlers = {
            "echo": self._echo,
            "openai": self._openai,
            "codex_cli": self._codex_cli,
            "ollama": self._ollama,
            "openai_compatible": self._openai_compatible,
        }
        if selected not in handlers:
            raise ProviderError(f"No adapter is installed for provider: {selected}")
        answer = handlers[selected](clean_message, settings)
        return {"provider": selected, "route": routed_by, "text": answer}

    def estimate_nutrition(self, image_data_url: str, note: str = "") -> dict[str, Any]:
        """Return a review-only food estimate without persisting the image or result."""
        settings = self.entries.get("openai", {})
        if not settings.get("enabled"):
            raise ProviderError("Enable the OpenAI provider before sending a food photo")
        if not re.match(r"^data:image/(?:jpeg|png|webp);base64,[A-Za-z0-9+/=]+$", image_data_url):
            raise ValueError("image must be a base64 JPEG, PNG, or WebP data URL")
        key_env = settings.get("api_key_env", "OPENAI_API_KEY")
        key = os.environ.get(key_env)
        if not key:
            raise ProviderError(f"Missing environment variable: {key_env}")
        model = os.environ.get(settings.get("model_env", "HERMES_OPENAI_MODEL")) or settings.get("default_model")
        result = _json_request(
            "https://api.openai.com/v1/responses",
            {
                "model": model,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Estimate the visible meal for owner review. Return JSON only with "
                                    "description, calories, protein_g, carbs_g, fat_g, fiber_g, "
                                    "sugar_g, sodium_mg, confidence (0 to 1), and notes. Use numeric "
                                    f"values and state key uncertainty in notes. Context: {note or 'none'}"
                                ),
                            },
                            {"type": "input_image", "image_url": image_data_url, "detail": "low"},
                        ],
                    }
                ],
                "store": False,
            },
            headers={"Authorization": f"Bearer {key}"},
        )
        raw = _responses_text(result).strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
        try:
            estimate = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProviderError("Food-photo provider returned invalid JSON") from exc
        if not isinstance(estimate, dict):
            raise ProviderError("Food-photo provider returned an invalid estimate")
        numeric = ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g", "sodium_mg")
        normalized = {
            key: max(0.0, float(estimate.get(key) or 0))
            for key in numeric
        }
        normalized.update(
            {
                "description": str(estimate.get("description") or "Food photo estimate").strip(),
                "confidence": max(0.0, min(1.0, float(estimate.get("confidence") or 0))),
                "notes": str(estimate.get("notes") or "Review portions before confirming.").strip(),
                "source": "provider_estimate",
                "status": "needs_review",
            }
        )
        return normalized

    @staticmethod
    def _echo(message: str, _settings: dict[str, Any]) -> str:
        return (
            "Hermes local starter is running. Configure OpenAI, Codex CLI, or "
            "Ollama when you want model-generated replies. Your message was: " + message
        )

    @staticmethod
    def _openai(message: str, settings: dict[str, Any]) -> str:
        key_env = settings.get("api_key_env", "OPENAI_API_KEY")
        key = os.environ.get(key_env)
        if not key:
            raise ProviderError(f"Missing environment variable: {key_env}")
        model_env = settings.get("model_env", "HERMES_OPENAI_MODEL")
        model = os.environ.get(model_env) or settings.get("default_model")
        if not model:
            raise ProviderError("No OpenAI model is configured")
        result = _json_request(
            "https://api.openai.com/v1/responses",
            {
                "model": model,
                "instructions": (
                    "You are the configured model provider for a local Hermes starter. "
                    "Answer the user's request directly. Never claim that local tools ran unless their results were supplied."
                ),
                "input": message,
                "store": False,
            },
            headers={"Authorization": f"Bearer {key}"},
        )
        return _responses_text(result)

    def _codex_cli(self, message: str, settings: dict[str, Any]) -> str:
        binary = shutil.which("codex")
        if not binary:
            raise ProviderError("Codex CLI is not installed")
        self.state_root.mkdir(parents=True, exist_ok=True)
        timeout = int(settings.get("timeout_seconds", 180))
        prompt = (
            "You are the model provider for a local Hermes starter dashboard. "
            "Return only a useful response to the user. This is a read-only chat turn; "
            "do not modify files or perform external writes.\n\nUser: " + message
        )
        with tempfile.TemporaryDirectory(prefix="hermes-codex-") as temp_dir:
            output_path = Path(temp_dir) / "final.txt"
            completed = subprocess.run(
                [
                    binary,
                    "exec",
                    "--ephemeral",
                    "--ignore-user-config",
                    "--sandbox",
                    "read-only",
                    "--skip-git-repo-check",
                    "--color",
                    "never",
                    "-C",
                    str(self.state_root),
                    "-o",
                    str(output_path),
                    prompt,
                ],
                text=True,
                capture_output=True,
                timeout=timeout,
            )
            if completed.returncode != 0 or not output_path.exists():
                raise ProviderError(f"Codex CLI exited with status {completed.returncode}")
            answer = output_path.read_text(encoding="utf-8").strip()
        if not answer:
            raise ProviderError("Codex CLI returned an empty response")
        return answer

    @staticmethod
    def _ollama(message: str, settings: dict[str, Any]) -> str:
        model_env = settings.get("model_env", "HERMES_OLLAMA_MODEL")
        model = os.environ.get(model_env) or settings.get("default_model")
        if not model:
            raise ProviderError(f"Missing local model; set {model_env}")
        base = str(settings.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
        result = _json_request(
            f"{base}/api/generate",
            {"model": model, "prompt": message, "stream": False},
        )
        answer = result.get("response")
        if not isinstance(answer, str) or not answer.strip():
            raise ProviderError("Ollama returned no text")
        return answer.strip()

    @staticmethod
    def _openai_compatible(message: str, settings: dict[str, Any]) -> str:
        base_env = settings.get("base_url_env", "HERMES_COMPAT_BASE_URL")
        key_env = settings.get("api_key_env", "HERMES_COMPAT_API_KEY")
        model_env = settings.get("model_env", "HERMES_COMPAT_MODEL")
        base = os.environ.get(base_env, "").rstrip("/")
        model = os.environ.get(model_env)
        if not base or not model:
            raise ProviderError(f"Set {base_env} and {model_env}")
        headers: dict[str, str] = {}
        if os.environ.get(key_env):
            headers["Authorization"] = f"Bearer {os.environ[key_env]}"
        result = _json_request(
            f"{base}/chat/completions",
            {"model": model, "messages": [{"role": "user", "content": message}]},
            headers=headers,
        )
        try:
            answer = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Compatible provider returned no message") from exc
        if not isinstance(answer, str) or not answer.strip():
            raise ProviderError("Compatible provider returned no text")
        return answer.strip()
