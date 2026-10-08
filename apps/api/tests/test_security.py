from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.core.config import Settings
from app.core.security import create_access_token, hash_password, verify_password, verify_token


def test_missing_jwt_secret_is_rejected(monkeypatch):
    monkeypatch.delenv('JWT_SECRET_KEY', raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_known_fallback_secret_is_rejected(monkeypatch):
    monkeypatch.setenv('JWT_SECRET_KEY', 'change-me-in-env')
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_short_jwt_secret_is_rejected():
    with pytest.raises(ValidationError):
        Settings(jwt_secret_key='short-secret', _env_file=None)


def test_password_hash_verifies_only_the_same_password():
    hashed = hash_password('password123')
    assert hashed != 'password123'
    assert verify_password('password123', hashed)
    assert not verify_password('password124', hashed)


def test_access_token_round_trip():
    token = create_access_token('15')
    assert verify_token(token) == 15


def test_tampered_token_is_rejected():
    token = create_access_token('15')
    header, payload, signature = token.split('.')
    replacement = 'A' if not signature.endswith('A') else 'B'
    tampered = f'{header}.{payload}.{signature[:-1]}{replacement}'
    with pytest.raises(HTTPException) as caught:
        verify_token(tampered)
    assert caught.value.status_code == 401


def test_expired_token_is_rejected():
    token = create_access_token('15', expires_minutes=-1)
    with pytest.raises(HTTPException) as caught:
        verify_token(token)
    assert caught.value.status_code == 401


def test_token_without_subject_is_rejected():
    from app.core.config import settings

    token = jwt.encode(
        {'exp': datetime.now(timezone.utc) + timedelta(minutes=5)},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(HTTPException) as caught:
        verify_token(token)
    assert caught.value.status_code == 401


def test_token_with_non_numeric_subject_is_rejected():
    from app.core.config import settings

    token = jwt.encode(
        {
            'sub': 'not-a-user-id',
            'exp': datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(HTTPException) as caught:
        verify_token(token)
    assert caught.value.status_code == 401
