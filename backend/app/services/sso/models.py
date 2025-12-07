from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    id: str
    login: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
