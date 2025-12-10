from pydantic import BaseModel, EmailStr, Field, constr

class RegisterSchema(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=2)

class LoginSchema(BaseModel):
    login: str
    password: str

class UpdatePasswordSchema(BaseModel):
    user_id: int
    new_password: str = Field(..., min_length=6)

class TokenUpdateSchema(BaseModel):
    refresh_token: str