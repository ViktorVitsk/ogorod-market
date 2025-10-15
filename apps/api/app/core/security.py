from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire_delta = timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode: dict[str, Any] = {'sub': subject, 'exp': expire}
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        subject: str = payload.get('sub')
        if subject is None:
            raise ValueError('Token subject missing')
        return int(subject)
    except jwt.PyJWTError as exc:  # type: ignore[attr-defined]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from exc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
