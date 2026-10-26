"""
Persistenza opzionale su Supabase via REST (PostgREST).
Se SUPABASE_URL / SUPABASE_ANON_KEY non sono impostate, tutto resta in memoria.
"""

from __future__ import annotations
import os
import json
from typing import Any, Optional

import httpx

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "") or os.environ.get("SUPABASE_SERVICE_KEY", "")


def enabled() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def create_game(state_json: dict) -> Optional[str]:
    if not enabled():
        return None
    payload = {
        "status": "active",
        "turn": state_json.get("turn", 1),
        "phase": state_json.get("phase", "MAIN"),
        "current_player": state_json.get("current_player", 0),
        "winner": state_json.get("winner"),
        "main_quest": state_json.get("main_quest"),
        "state_json": state_json,
    }
    try:
        r = httpx.post(
            f"{SUPABASE_URL}/rest/v1/games",
            headers=_headers(),
            json=payload,
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return data[0].get("id")
        if isinstance(data, dict):
            return data.get("id")
    except Exception as e:
        print(f"[supabase] create_game error: {e}")
    return None


def update_game(game_id: str, state_json: dict) -> bool:
    if not enabled() or not game_id:
        return False
    payload = {
        "updated_at": "now()",
        "status": "finished" if state_json.get("winner") is not None else "active",
        "turn": state_json.get("turn", 1),
        "phase": state_json.get("phase", "MAIN"),
        "current_player": state_json.get("current_player", 0),
        "winner": state_json.get("winner"),
        "main_quest": state_json.get("main_quest"),
        "state_json": state_json,
    }
    # PostgREST non accetta "now()" come stringa in JSON per timestamptz facilmente:
    # inviamo updated_at omesso e usiamo un trigger, oppure ISO timestamp lato client.
    from datetime import datetime, timezone
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    try:
        r = httpx.patch(
            f"{SUPABASE_URL}/rest/v1/games?id=eq.{game_id}",
            headers=_headers(),
            json=payload,
            timeout=15,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[supabase] update_game error: {e}")
        return False


def log_move(game_id: str, player_id: int, action: str, payload: dict) -> None:
    if not enabled() or not game_id:
        return
    try:
        httpx.post(
            f"{SUPABASE_URL}/rest/v1/game_moves",
            headers=_headers(),
            json={
                "game_id": game_id,
                "player_id": player_id,
                "action": action,
                "payload": payload,
            },
            timeout=10,
        )
    except Exception as e:
        print(f"[supabase] log_move error: {e}")
