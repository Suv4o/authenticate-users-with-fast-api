import re
from typing import Optional
from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status


class CreateUser(BaseModel):
    email: str = None
    full_name: str = None
    password: str = None

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


class UserInDB(BaseModel):
    id: int
    email: str = None
    full_name: str = None
    disabled: Optional[bool] = None
    password: str
    refresh_token: Optional[str] = None
    created_at: str
    updated_at: str
