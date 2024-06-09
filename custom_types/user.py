from typing import Optional
from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str = None
    full_name: str = None
    password: str = None


class UserInDB(BaseModel):
    id: int
    email: str = None
    full_name: str = None
    disabled: Optional[bool] = None
    password: str
    refresh_token: Optional[str] = None
    created_at: str
    updated_at: str
