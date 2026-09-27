from datetime import UTC, datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from dormitory_infrastructure.persistence.config import get_settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str, role: str, email: str) -> str:
    settings = get_settings()
    expires = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "email": email,
        "role": role,
        "jti": str(uuid4()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": datetime.now(UTC),
        "exp": expires,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def create_refresh_token() -> str:
    return token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
