"""
Auth Supabase JWT (Fase 4.1 – base per 4.2).

Verifica il Bearer token emesso da Supabase Auth.
- Con SUPABASE_JWT_SECRET: verifica locale HS256 (consigliato in produzione API).
- Altrimenti: chiama GET /auth/v1/user con il token (più semplice, 1 HTTP extra).

Uso (step 4.2):
    from api.auth_supabase import require_user
    user = require_user(authorization_header)
    # user["id"] = uuid string
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "") or os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")


class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def enabled() -> bool:
    return bool(SUPABASE_URL and (SUPABASE_JWT_SECRET or SUPABASE_ANON_KEY))


def _parse_bearer(authorization: Optional[str]) -> str:
    if not authorization:
        raise AuthError("Missing Authorization header")
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthError("Expected Bearer token")
    token = parts[1].strip()
    if not token:
        raise AuthError("Empty Bearer token")
    return token


def _verify_local(token: str) -> Dict[str, Any]:
    """Verifica JWT con secret progetto (Settings → API → JWT Secret)."""
    try:
        from jose import jwt, JWTError  # type: ignore
    except ImportError as e:
        raise AuthError(
            "PyJWT/python-jose non installato: aggiungi python-jose[cryptography] a requirements.txt",
            status_code=500,
        ) from e
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except Exception as e:
        raise AuthError(f"Invalid token: {e}") from e
    uid = payload.get("sub")
    if not uid:
        raise AuthError("Token senza sub")
    return {
        "id": uid,
        "email": payload.get("email"),
        "role": payload.get("role"),
        "raw": payload,
    }


def _verify_remote(token: str) -> Dict[str, Any]:
    """Fallback: chiede a Supabase chi è l'utente."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise AuthError("SUPABASE_URL / ANON_KEY mancanti", status_code=500)
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
        raise AuthError(f"Auth service error: {e}", status_code=503) from e
    if r.status_code != 200:
        raise AuthError("Invalid or expired token")
    data = r.json()
    uid = data.get("id")
    if not uid:
        raise AuthError("User payload senza id")
    return {
        "id": uid,
        "email": data.get("email"),
        "role": data.get("role"),
        "raw": data,
    }


def verify_token(token: str) -> Dict[str, Any]:
    if SUPABASE_JWT_SECRET:
        return _verify_local(token)
    return _verify_remote(token)


def require_user(authorization: Optional[str]) -> Dict[str, Any]:
    """Solleva AuthError se non autenticato."""
    token = _parse_bearer(authorization)
    return verify_token(token)


def optional_user(authorization: Optional[str]) -> Optional[Dict[str, Any]]:
    if not authorization:
        return None
    try:
        return require_user(authorization)
    except AuthError:
        return None
