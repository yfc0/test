from pydantic import BaseModel

from datetime import date


class CreateCode(BaseModel):
    end_date: date


class CreateUser(BaseModel):
    username: str
    password: str
    email: str
    code: str | None


class AuthUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: int | None
