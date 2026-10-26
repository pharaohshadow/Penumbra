"""
Persistenza opzionale su Supabase via REST (PostgREST).
4.2.3 – supporto scrittura ownership (player0_uid, player1_uid, p1_is_ai).
"""

from __future__ import annotations
import os
from typing import Any, Optional, Dict
from datetime import datetime, timezone

import httpx

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "") or os.environ.get("SUPABASE_SERVICE_KEY", "")


def enabled() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _headers(prefer: str = "return=representation") -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": prefer,
    }


def create_game(
    state_json: dict,
    game_id: Optional[str] = None,
    player0_uid: Optional[str] = None,
    player1_uid: Optional[str] = None,
    p1_is_ai: bool = True,
) -> Optional[str]:
    """
    Crea una partita. Se passati, salva anche gli uid di ownership.
    """
    if not enabled():
        return None
    payload: Dict[str, Any] = {
        "status": "finished" if state_json.get("winner") is not None else "active",
        "turn": state_json.get("turn", 1),
        "phase": state_json.get("phase", "MAIN"),
        "current_player": state_json.get("current_player", 0),
        "winner": state_json.get("winner"),
        "main_quest": state_json.get("main_quest"),
        "state_json": state_json,
        "p1_is_ai": p1_is_ai,
    }
    if game_id:
        payload["id"] = game_id
    if player0_uid is not None:
        payload["player0_uid"] = player0_uid
    if player1_uid is not None:
        payload["player1_uid"] = player1_uid
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


def update_game(
    game_id: str,
    state_json: dict,
    player0_uid: Optional[str] = None,
    player1_uid: Optional[str] = None,
    p1_is_ai: Optional[bool] = None,
) -> bool:
    """
    Aggiorna stato partita. Se passati, aggiorna anche i campi ownership.
    """
    if not enabled() or not game_id:
        return False
    payload: Dict[str, Any] = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "finished" if state_json.get("winner") is not None else "active",
        "turn": state_json.get("turn", 1),
        "phase": state_json.get("phase", "MAIN"),
        "current_player": state_json.get("current_player", 0),
        "winner": state_json.get("winner"),
        "main_quest": state_json.get("main_quest"),
        "state_json": state_json,
    }
    if player0_uid is not None:
        payload["player0_uid"] = player0_uid
    if player1_uid is not None:
        payload["player1_uid"] = player1_uid
    if p1_is_ai is not None:
        payload["p1_is_ai"] = p1_is_ai
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


def set_ownership(
    game_id: str,
    player0_uid: Optional[str] = None,
    player1_uid: Optional[str] = None,
    p1_is_ai: Optional[bool] = None,
) -> bool:
    """
    Aggiorna solo i campi di ownership (senza toccare state_json).
    Utile quando qualcuno si unisce (join) o si assegna il creatore.
    """
    if not enabled() or not game_id:
        return False
    payload: Dict[str, Any] = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if player0_uid is not None:
        payload["player0_uid"] = player0_uid
    if player1_uid is not None:
        payload["player1_uid"] = player1_uid
    if p1_is_ai is not None:
        payload["p1_is_ai"] = p1_is_ai
    if len(payload) == 1:
        # solo updated_at → niente da fare
        return True
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
        print(f"[supabase] set_ownership error: {e}")
        return False


def fetch_game(game_id: str) -> Optional[Dict[str, Any]]:
    """Ritorna la riga games (con state_json e ownership) oppure None."""
    if not enabled() or not game_id:
        return None
    try:
        r = httpx.get(
            f"{SUPABASE_URL}/rest/v1/games?id=eq.{game_id}&select=*",
            headers=_headers(),
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return data[0]
    except Exception as e:
        print(f"[supabase] fetch_game error: {e}")
    return None


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
