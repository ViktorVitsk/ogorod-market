from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


PasswordStr = Annotated[str, StringConstraints(min_length=8)]


class UserCreate(BaseModel):
    email: EmailStr
    password: PasswordStr
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: str
    exp: int
