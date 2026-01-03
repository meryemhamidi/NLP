"""Tools to read/write user memory profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


STORE_PATH = Path(__file__).resolve().parent.parent / ".adk" / "artifacts" / "user_memory.json"


def _load_store() -> dict:
    if STORE_PATH.exists():
        try:
            return json.loads(STORE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_store(data: dict) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def remember_user_profile(
    user_id: str, preferences: dict, override: bool = False
) -> dict:
    """Persist user preferences (user memory across sessions)."""
    data = _load_store()
    if not override and user_id in data:
        merged = {**data[user_id], **preferences}
    else:
        merged = preferences
    data[user_id] = merged
    _save_store(data)
    return {"status": "stored", "user_id": user_id, "profile": merged}


def get_user_profile(user_id: str, field: Optional[str] = None) -> dict:
    """Retrieve stored preferences for a user."""
    data = _load_store()
    profile = data.get(user_id, {})
    if field:
        return {"user_id": user_id, field: profile.get(field)}
    return {"user_id": user_id, "profile": profile}
