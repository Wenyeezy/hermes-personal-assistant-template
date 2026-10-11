"""Explicit, isolated fictional data for a first-run walkthrough."""

from __future__ import annotations

import json
from datetime import date

from .config import RuntimePaths, load_config
from .store import HermesStore


def seed_demo(paths: RuntimePaths) -> bool:
    config = load_config(paths)
    entries = config.get("providers", {}).get("entries", {})
    if config.get("providers", {}).get("default") != "echo" or any(
        value.get("enabled") for name, value in entries.items() if name != "echo"
    ):
        raise ValueError("Fictional demo requires an offline-only config. Choose a fresh --root.")
    store = HermesStore(paths.database)
    marker = paths.root / ".fictional-demo.json"
    if marker.exists():
        record = json.loads(marker.read_text(encoding="utf-8"))
        if record.get("schema") != "hermes.fictional-demo.v1":
            raise ValueError("Unknown demo marker; choose a fresh --root.")
        return False
    if any(store.recent(module, limit=1) for module in ("nutrition", "health", "workouts", "finance", "career")):
        raise ValueError("Refusing to mix fictional samples with existing records. Choose a fresh --root.")
    day = date.today().isoformat()
    store.add_nutrition({"occurred_on": day, "description": "Fictional sample: oat bowl", "calories": 420, "protein_g": 18, "fiber_g": 7, "source": "manual", "status": "confirmed", "notes": "Made-up demonstration, not a real meal."})
    store.add_nutrition({"occurred_on": day, "description": "Fictional sample: lunch estimate", "calories": 610, "protein_g": 28, "source": "provider_estimate", "status": "needs_review", "notes": "Scripted sample; no model was called. Excluded from confirmed totals."})
    store.add_health({"occurred_on": day, "steps": 6800, "exercise_minutes": 30, "source": "fictional_demo"})
    store.add_finance({"occurred_on": day, "description": "Fictional sample: notebook", "amount": 12, "category": "supplies", "status": "needs_review"})
    store.add_career({"company": "Harbor Works (fictional)", "role": "Product Operations", "status": "reviewing", "next_step": "Compare the role with your priorities; no application is sent."})
    marker.write_text(json.dumps({"schema": "hermes.fictional-demo.v1", "fictional": True, "day": day}, indent=2) + "\n", encoding="utf-8")
    return True
