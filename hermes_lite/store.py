"""Local SQLite stores for the sanitized Hermes starter modules."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class HermesStore:
    def __init__(self, database: str | Path):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS nutrition_events (
                    id TEXT PRIMARY KEY,
                    occurred_on TEXT NOT NULL,
                    description TEXT NOT NULL,
                    calories REAL NOT NULL DEFAULT 0,
                    protein_g REAL NOT NULL DEFAULT 0,
                    carbs_g REAL NOT NULL DEFAULT 0,
                    fat_g REAL NOT NULL DEFAULT 0,
                    fiber_g REAL NOT NULL DEFAULT 0,
                    sugar_g REAL NOT NULL DEFAULT 0,
                    sodium_mg REAL NOT NULL DEFAULT 0,
                    meal_type TEXT NOT NULL DEFAULT 'unspecified',
                    source TEXT NOT NULL DEFAULT 'manual',
                    confidence REAL,
                    notes TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'confirmed',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS health_daily (
                    occurred_on TEXT PRIMARY KEY,
                    steps INTEGER,
                    active_calories REAL,
                    resting_calories REAL,
                    exercise_minutes REAL,
                    standing_minutes REAL,
                    distance_km REAL,
                    sleep_hours REAL,
                    weight_kg REAL,
                    source TEXT NOT NULL DEFAULT 'manual',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS health_workouts (
                    id TEXT PRIMARY KEY,
                    occurred_on TEXT NOT NULL,
                    activity TEXT NOT NULL,
                    duration_minutes REAL NOT NULL DEFAULT 0,
                    active_calories REAL,
                    distance_km REAL,
                    source_id TEXT NOT NULL DEFAULT '',
                    source TEXT NOT NULL DEFAULT 'manual',
                    created_at TEXT NOT NULL,
                    UNIQUE(source, source_id)
                );
                CREATE TABLE IF NOT EXISTS nutrition_goals (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    calories REAL,
                    protein_g REAL,
                    carbs_g REAL,
                    fat_g REAL,
                    fiber_g REAL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS finance_entries (
                    id TEXT PRIMARY KEY,
                    occurred_on TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL DEFAULT 'uncategorized',
                    status TEXT NOT NULL DEFAULT 'needs_review',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS career_opportunities (
                    id TEXT PRIMARY KEY,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'saved',
                    url TEXT NOT NULL DEFAULT '',
                    next_step TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS chat_events (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            self._ensure_columns(
                db,
                "nutrition_events",
                {
                    "fiber_g": "REAL NOT NULL DEFAULT 0",
                    "sugar_g": "REAL NOT NULL DEFAULT 0",
                    "sodium_mg": "REAL NOT NULL DEFAULT 0",
                    "meal_type": "TEXT NOT NULL DEFAULT 'unspecified'",
                    "source": "TEXT NOT NULL DEFAULT 'manual'",
                    "confidence": "REAL",
                    "notes": "TEXT NOT NULL DEFAULT ''",
                },
            )
            self._ensure_columns(
                db,
                "health_daily",
                {
                    "standing_minutes": "REAL",
                    "distance_km": "REAL",
                    "sleep_hours": "REAL",
                    "weight_kg": "REAL",
                },
            )

    @staticmethod
    def _ensure_columns(
        db: sqlite3.Connection, table: str, columns: dict[str, str]
    ) -> None:
        existing = {row["name"] for row in db.execute(f"PRAGMA table_info({table})")}
        for name, definition in columns.items():
            if name not in existing:
                db.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")

    @staticmethod
    def _required_text(value: Any, label: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValueError(f"{label} is required")
        return text

    @staticmethod
    def _day(value: Any) -> str:
        raw = str(value or date.today().isoformat()).strip()
        return date.fromisoformat(raw).isoformat()

    @staticmethod
    def _number(value: Any, label: str, *, optional: bool = False) -> float | None:
        if optional and (value is None or value == ""):
            return None
        try:
            return float(value or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{label} must be a number") from exc

    def add_nutrition(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = {
            "id": uuid.uuid4().hex,
            "occurred_on": self._day(payload.get("occurred_on")),
            "description": self._required_text(payload.get("description"), "description"),
            "calories": self._number(payload.get("calories"), "calories"),
            "protein_g": self._number(payload.get("protein_g"), "protein_g"),
            "carbs_g": self._number(payload.get("carbs_g"), "carbs_g"),
            "fat_g": self._number(payload.get("fat_g"), "fat_g"),
            "fiber_g": self._number(payload.get("fiber_g"), "fiber_g"),
            "sugar_g": self._number(payload.get("sugar_g"), "sugar_g"),
            "sodium_mg": self._number(payload.get("sodium_mg"), "sodium_mg"),
            "meal_type": str(payload.get("meal_type") or "unspecified").strip(),
            "source": str(payload.get("source") or "manual").strip(),
            "confidence": self._number(payload.get("confidence"), "confidence", optional=True),
            "notes": str(payload.get("notes") or "").strip(),
            "status": str(payload.get("status") or "confirmed"),
            "created_at": utc_now(),
        }
        with self.connect() as db:
            db.execute(
                """INSERT INTO nutrition_events
                (id, occurred_on, description, calories, protein_g, carbs_g, fat_g,
                 fiber_g, sugar_g, sodium_mg, meal_type, source, confidence, notes,
                 status, created_at)
                VALUES (:id, :occurred_on, :description, :calories, :protein_g,
                 :carbs_g, :fat_g, :fiber_g, :sugar_g, :sodium_mg, :meal_type,
                 :source, :confidence, :notes, :status, :created_at)""",
                row,
            )
        return row

    def add_health(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = {
            "occurred_on": self._day(payload.get("occurred_on")),
            "steps": self._number(payload.get("steps"), "steps", optional=True),
            "active_calories": self._number(payload.get("active_calories"), "active_calories", optional=True),
            "resting_calories": self._number(payload.get("resting_calories"), "resting_calories", optional=True),
            "exercise_minutes": self._number(payload.get("exercise_minutes"), "exercise_minutes", optional=True),
            "standing_minutes": self._number(payload.get("standing_minutes"), "standing_minutes", optional=True),
            "distance_km": self._number(payload.get("distance_km"), "distance_km", optional=True),
            "sleep_hours": self._number(payload.get("sleep_hours"), "sleep_hours", optional=True),
            "weight_kg": self._number(payload.get("weight_kg"), "weight_kg", optional=True),
            "source": str(payload.get("source") or "manual"),
            "created_at": utc_now(),
        }
        with self.connect() as db:
            db.execute(
                """INSERT INTO health_daily
                (occurred_on, steps, active_calories, resting_calories, exercise_minutes,
                 standing_minutes, distance_km, sleep_hours, weight_kg, source, created_at)
                VALUES (:occurred_on, :steps, :active_calories, :resting_calories,
                 :exercise_minutes, :standing_minutes, :distance_km, :sleep_hours,
                 :weight_kg, :source, :created_at)
                ON CONFLICT(occurred_on) DO UPDATE SET
                  steps=excluded.steps, active_calories=excluded.active_calories,
                  resting_calories=excluded.resting_calories,
                  exercise_minutes=excluded.exercise_minutes,
                  standing_minutes=COALESCE(excluded.standing_minutes, health_daily.standing_minutes),
                  distance_km=COALESCE(excluded.distance_km, health_daily.distance_km),
                  sleep_hours=COALESCE(excluded.sleep_hours, health_daily.sleep_hours),
                  weight_kg=COALESCE(excluded.weight_kg, health_daily.weight_kg),
                  source=excluded.source, created_at=excluded.created_at""",
                row,
            )
        return row

    def add_workout(self, payload: dict[str, Any], *, source: str = "manual") -> dict[str, Any]:
        event_time = str(payload.get("event_time") or payload.get("occurred_on") or "")
        occurred_on = self._day(event_time[:10] if event_time else None)
        source_id = str(payload.get("source_id") or "").strip()
        row = {
            "id": uuid.uuid4().hex,
            "occurred_on": occurred_on,
            "activity": self._required_text(payload.get("activity"), "activity"),
            "duration_minutes": self._number(
                payload.get("duration_minutes", payload.get("duration_min")),
                "duration_minutes",
            ),
            "active_calories": self._number(payload.get("active_calories"), "active_calories", optional=True),
            "distance_km": self._number(
                payload.get("distance_km", payload.get("distance")), "distance_km", optional=True
            ),
            "source_id": source_id,
            "source": source,
            "created_at": utc_now(),
        }
        with self.connect() as db:
            if source_id:
                existing = db.execute(
                    "SELECT * FROM health_workouts WHERE source=? AND source_id=?",
                    (source, source_id),
                ).fetchone()
                if existing:
                    return dict(existing)
            db.execute(
                """INSERT INTO health_workouts
                (id, occurred_on, activity, duration_minutes, active_calories,
                 distance_km, source_id, source, created_at)
                VALUES (:id, :occurred_on, :activity, :duration_minutes,
                 :active_calories, :distance_km, :source_id, :source, :created_at)""",
                row,
            )
        return row

    def import_health(self, payload: dict[str, Any]) -> dict[str, Any]:
        daily = payload.get("daily") if isinstance(payload.get("daily"), dict) else payload
        source = str(payload.get("source") or daily.get("source") or "health_import")
        normalized = dict(daily)
        normalized["occurred_on"] = daily.get("date") or daily.get("occurred_on")
        normalized["exercise_minutes"] = daily.get("exercise_min", daily.get("exercise_minutes"))
        normalized["source"] = source
        saved_daily = self.add_health(normalized)
        saved_workouts = [
            self.add_workout(item, source=source)
            for item in payload.get("workouts", [])
            if isinstance(item, dict)
        ]
        return {"daily": saved_daily, "workouts": saved_workouts}

    def set_nutrition_goals(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = {
            key: self._number(payload.get(key), key, optional=True)
            for key in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g")
        }
        row["updated_at"] = utc_now()
        with self.connect() as db:
            db.execute(
                """INSERT INTO nutrition_goals
                (id, calories, protein_g, carbs_g, fat_g, fiber_g, updated_at)
                VALUES (1, :calories, :protein_g, :carbs_g, :fat_g, :fiber_g, :updated_at)
                ON CONFLICT(id) DO UPDATE SET calories=excluded.calories,
                protein_g=excluded.protein_g, carbs_g=excluded.carbs_g,
                fat_g=excluded.fat_g, fiber_g=excluded.fiber_g,
                updated_at=excluded.updated_at""",
                row,
            )
        return row

    def nutrition_summary(self, start: str, end: str) -> dict[str, Any]:
        start_day, end_day = self._day(start), self._day(end)
        if start_day > end_day:
            raise ValueError("start must not be after end")
        with self.connect() as db:
            totals = dict(
                db.execute(
                    """SELECT COUNT(*) AS entries,
                    COALESCE(SUM(calories),0) AS calories,
                    COALESCE(SUM(protein_g),0) AS protein_g,
                    COALESCE(SUM(carbs_g),0) AS carbs_g,
                    COALESCE(SUM(fat_g),0) AS fat_g,
                    COALESCE(SUM(fiber_g),0) AS fiber_g,
                    COALESCE(SUM(sugar_g),0) AS sugar_g,
                    COALESCE(SUM(sodium_mg),0) AS sodium_mg
                    FROM nutrition_events
                    WHERE occurred_on BETWEEN ? AND ? AND status='confirmed'""",
                    (start_day, end_day),
                ).fetchone()
            )
            goal_row = db.execute("SELECT * FROM nutrition_goals WHERE id=1").fetchone()
        return {
            "start": start_day,
            "end": end_day,
            "totals": totals,
            "goals": dict(goal_row) if goal_row else None,
        }

    def health_summary(self, limit: int = 7) -> dict[str, Any]:
        with self.connect() as db:
            days = [
                dict(row)
                for row in db.execute(
                    "SELECT * FROM health_daily ORDER BY occurred_on DESC LIMIT ?",
                    (max(1, min(limit, 90)),),
                ).fetchall()
            ]
            workouts = [
                dict(row)
                for row in db.execute(
                    "SELECT * FROM health_workouts ORDER BY occurred_on DESC, created_at DESC LIMIT 50"
                ).fetchall()
            ]
        return {"days": days, "workouts": workouts}

    def nutrition_health_export(self, target_day: str) -> dict[str, Any]:
        day = self._day(target_day)
        summary = self.nutrition_summary(day, day)["totals"]
        mapping = {
            "calories": ("dietaryEnergyConsumed", "kcal"),
            "protein_g": ("dietaryProtein", "g"),
            "carbs_g": ("dietaryCarbohydrates", "g"),
            "fat_g": ("dietaryFatTotal", "g"),
            "fiber_g": ("dietaryFiber", "g"),
            "sugar_g": ("dietarySugar", "g"),
            "sodium_mg": ("dietarySodium", "mg"),
        }
        samples = [
            {"healthkit_identifier": identifier, "value": summary[key], "unit": unit, "date": day}
            for key, (identifier, unit) in mapping.items()
            if summary[key]
        ]
        return {"date": day, "source": "hermes_confirmed_nutrition", "samples": samples}

    def add_finance(self, payload: dict[str, Any]) -> dict[str, Any]:
        row = {
            "id": uuid.uuid4().hex,
            "occurred_on": self._day(payload.get("occurred_on")),
            "description": self._required_text(payload.get("description"), "description"),
            "amount": self._number(payload.get("amount"), "amount"),
            "category": str(payload.get("category") or "uncategorized").strip(),
            "status": str(payload.get("status") or "needs_review"),
            "created_at": utc_now(),
        }
        with self.connect() as db:
            db.execute(
                """INSERT INTO finance_entries
                (id, occurred_on, description, amount, category, status, created_at)
                VALUES (:id, :occurred_on, :description, :amount, :category, :status, :created_at)""",
                row,
            )
        return row

    def add_career(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = utc_now()
        row = {
            "id": uuid.uuid4().hex,
            "company": self._required_text(payload.get("company"), "company"),
            "role": self._required_text(payload.get("role"), "role"),
            "status": str(payload.get("status") or "saved"),
            "url": str(payload.get("url") or "").strip(),
            "next_step": str(payload.get("next_step") or "").strip(),
            "created_at": now,
            "updated_at": now,
        }
        with self.connect() as db:
            db.execute(
                """INSERT INTO career_opportunities
                (id, company, role, status, url, next_step, created_at, updated_at)
                VALUES (:id, :company, :role, :status, :url, :next_step, :created_at, :updated_at)""",
                row,
            )
        return row

    def add_chat(self, session_id: str, provider: str, role: str, content: str) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO chat_events VALUES (?, ?, ?, ?, ?, ?)",
                (uuid.uuid4().hex, session_id, provider, role, content, utc_now()),
            )

    def recent(self, table: str, *, limit: int = 20) -> list[dict[str, Any]]:
        allowed = {
            "nutrition": ("nutrition_events", "occurred_on DESC, created_at DESC"),
            "health": ("health_daily", "occurred_on DESC"),
            "workouts": ("health_workouts", "occurred_on DESC, created_at DESC"),
            "finance": ("finance_entries", "occurred_on DESC, created_at DESC"),
            "career": ("career_opportunities", "updated_at DESC"),
        }
        if table not in allowed:
            raise ValueError("unknown module")
        name, order = allowed[table]
        with self.connect() as db:
            rows = db.execute(
                f"SELECT * FROM {name} ORDER BY {order} LIMIT ?", (max(1, min(limit, 100)),)
            ).fetchall()
        return [dict(row) for row in rows]

    def dashboard(self) -> dict[str, Any]:
        today = date.today().isoformat()
        with self.connect() as db:
            nutrition = self.nutrition_summary(today, today)["totals"]
            health_row = db.execute(
                "SELECT * FROM health_daily ORDER BY occurred_on DESC LIMIT 1"
            ).fetchone()
            finance = dict(
                db.execute(
                    """SELECT COUNT(*) AS entries, COALESCE(SUM(amount),0) AS total,
                    COALESCE(SUM(CASE WHEN status='needs_review' THEN 1 ELSE 0 END),0) AS needs_review
                    FROM finance_entries"""
                ).fetchone()
            )
            career = {
                row["status"]: row["count"]
                for row in db.execute(
                    "SELECT status, COUNT(*) AS count FROM career_opportunities GROUP BY status"
                ).fetchall()
            }
        return {
            "nutrition": nutrition,
            "health": dict(health_row) if health_row else None,
            "finance": finance,
            "career": career,
        }
