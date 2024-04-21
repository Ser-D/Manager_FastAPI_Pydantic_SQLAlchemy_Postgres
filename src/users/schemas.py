from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6, max_length=8)


class UserResponseSchema(BaseModel):
    id: int = 1
    username: str
    email: str | None
    avatar: str

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LogoutResponse(BaseModel):
    result: str


class RequestEmail(BaseModel):
    email: str