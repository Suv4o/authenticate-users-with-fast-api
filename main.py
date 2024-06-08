from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import timedelta
from jose import jwt
from config.env import env
from custom_types import User, Token
from utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_user,
    verify_refresh_token,
    db,
)

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = env["ACCESS_TOKEN_EXPIRE_MINUTES"]
REFRESH_TOKEN_EXPIRE_DAYS = env["REFRESH_TOKEN_EXPIRE_DAYS"]


app = FastAPI()


# TODO: Move this to separate router
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    if not user.refresh_token or not verify_refresh_token(user.refresh_token):
        refresh_token = create_refresh_token(data={"sub": user.username})
        user.refresh_token = refresh_token
    else:
        refresh_token = user.refresh_token

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


# TODO: Move this to separate router
@app.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    if not verify_refresh_token(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    user = get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


# TODO: Move this to separate router
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# TODO: Move this to separate router
@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]
