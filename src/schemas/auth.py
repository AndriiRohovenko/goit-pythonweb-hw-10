from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    birthdate: Optional[date] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
