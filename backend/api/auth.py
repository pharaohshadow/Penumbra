"""
4.2.2 – Modulo verifica JWT Supabase (require_user).

- Preferito: verifica locale HS256 con SUPABASE_JWT_SECRET
- Fallback: GET /auth/v1/user (se il secret non è impostato)
- Nessun ALLOW_ANON_PLAY / ALLOW_LEGACY_OPEN (scelta A, sito in costruzione)
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx
from fastapi import Header, HTTPException

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "") or os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")


def auth_configured() -> bool:
    return bool(SUPABASE_URL and (SUPABASE_JWT_SECRET or SUPABASE_ANON_KEY))


def parse_bearer(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1].strip()
    return token or None


def _verify_local(token: str) -> Dict[str, Any]:
    try:
        from jose import jwt  # type: ignore
    except ImportError as e:
        raise HTTPException(
            500,
            "python-jose non installato: aggiungi python-jose[cryptography] a requirements.txt",
        ) from e
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except Exception as e:
        raise HTTPException(401, f"Token non valido: {e}") from e
    uid = payload.get("sub")
    if not uid:
        raise HTTPException(401, "Token senza sub")
    return {
        "id": uid,
        "email": payload.get("email"),
        "role": payload.get("role"),
        "raw": payload,
    }


def _verify_remote(token: str) -> Dict[str, Any]:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(503, "Auth non configurata (mancano SUPABASE_URL / ANON_KEY)")
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
    uid = data.get("id")
    if not uid:
        raise HTTPException(401, "Token senza user id")
    return {
        "id": uid,
        "email": data.get("email"),
        "role": data.get("role"),
        "raw": data,
    }


def verify_access_token(token: str) -> Dict[str, Any]:
    if not auth_configured():
        raise HTTPException(503, "Auth non configurata")
    if SUPABASE_JWT_SECRET:
        return _verify_local(token)
    return _verify_remote(token)


async def require_user(
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    """
    Dependency FastAPI.
    Ritorna dict con almeno {"id": "<uuid>"}.
    Solleva 401 se token assente/invalido.
    """
    token = parse_bearer(authorization)
    if not token:
        raise HTTPException(401, "Authorization Bearer richiesto")
    return verify_access_token(token)


def user_id(user: Optional[Dict[str, Any]]) -> Optional[str]:
    if not user:
        return None
    return user.get("id")
