"""
Auth Supabase JWT per Penumbra 4.2.

Verifica il Bearer token con GET /auth/v1/user (non serve JWT secret nel backend).
"""

from __future__ import annotations
import os
from typing import Any, Dict, Optional

import httpx
from fastapi import Header, HTTPException

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
# Emergenza/dev: se true, le route accettano anche richieste senza Bearer
ALLOW_ANON_PLAY = os.environ.get("ALLOW_ANON_PLAY", "").lower() in ("1", "true", "yes")


def auth_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_ANON_KEY)


def verify_access_token(token: str) -> Dict[str, Any]:
    if not auth_configured():
        raise HTTPException(503, "Auth non configurata (mancano SUPABASE_URL / SUPABASE_ANON_KEY)")
    if not token:
        raise HTTPException(401, "Token mancante")
    try:
        r = httpx.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except Exception as e:
        raise HTTPException(503, f"Auth service unreachable: {e}") from e
    if r.status_code != 200:
        raise HTTPException(401, "Token non valido o scaduto")
    data = r.json()
    if not data.get("id"):
        raise HTTPException(401, "Token senza user id")
    return data


def parse_bearer(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None


async def require_user(
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    """JWT obbligatorio, salvo ALLOW_ANON_PLAY."""
    token = parse_bearer(authorization)
    if not token:
        if ALLOW_ANON_PLAY:
            return {"id": None, "email": None, "anon": True}
        raise HTTPException(401, "Authorization Bearer richiesto")
    return verify_access_token(token)


def user_id(user: Optional[Dict[str, Any]]) -> Optional[str]:
    if not user or user.get("anon"):
        return None
    return user.get("id")
