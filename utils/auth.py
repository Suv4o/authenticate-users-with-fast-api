import logging
from typing import Optional, Union
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from custom_types import UserInDB, TokenData
from passlib.context import CryptContext
from jose import jwt, JWTError
from config.env import env
from config.database import get_db
from models import Users

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = env["ACCESS_TOKEN_EXPIRE_MINUTES"]
REFRESH_TOKEN_EXPIRE_DAYS = env["REFRESH_TOKEN_EXPIRE_DAYS"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logging.getLogger("passlib").setLevel(logging.ERROR)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    user = db.query(Users).filter(Users.email == email).first()

    return user


def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return False
        return True
    except JWTError:
        return False


def create_access_token(
    data: dict, expires_delta: Optional[Union[timedelta, None]] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception

    user = get_user(db, email=token_data.email)

    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
