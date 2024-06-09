from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from datetime import timedelta
from jose import jwt
from config.env import env
from custom_types import Token, OAuth2PasswordRequestForm as OAuth2RequestForm
from utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_user,
    verify_refresh_token,
)

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = env["ACCESS_TOKEN_EXPIRE_MINUTES"]
REFRESH_TOKEN_EXPIRE_DAYS = env["REFRESH_TOKEN_EXPIRE_DAYS"]


router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@router.post("", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2RequestForm = Depends(), db: Session = Depends(get_db)
):

    email = form_data.username
    password = form_data.password
    refresh_token = None

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    if not user.refresh_token or not verify_refresh_token(user.refresh_token):
        refresh_token = create_refresh_token(data={"sub": user.email})

        user_to_update = get_user(db, email)
        user_to_update.refresh_token = refresh_token
        db.commit()

    else:
        refresh_token = user.refresh_token

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    if not verify_refresh_token(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    user = get_user(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }
