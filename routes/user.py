from fastapi import Depends, APIRouter, HTTPException, status
from custom_types import CreateUser, UserInDB
from models import Users
from sqlalchemy.orm import Session
from config.database import get_db
from utils import (
    get_current_active_user,
    get_password_hash,
)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("")
async def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    db_user = db.query(Users).filter(Users.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    full_name = user.full_name
    email = user.email
    password = get_password_hash(user.password)

    db_user = Users(full_name=full_name, email=email, password=password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.uid,
        "email": db_user.email,
        "full_name": db_user.full_name,
        "disabled": db_user.disabled,
    }
