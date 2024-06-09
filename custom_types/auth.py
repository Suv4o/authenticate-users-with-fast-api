import re
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None


class OAuth2PasswordRequestForm(BaseModel):
    username: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        try:
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not re.search("[A-Z]", password):
                raise ValueError("Password must contain at least one uppercase letter")
            if not re.search("[a-z]", password):
                raise ValueError("Password must contain at least one lowercase letter")
            if not re.search("[0-9]", password):
                raise ValueError("Password must contain at least one digit")
            if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
                raise ValueError("Password must contain at least one special character")
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
            )
        return password
