import routes.token as token
from fastapi import Depends, FastAPI
from custom_types import User
from utils import (
    get_current_active_user,
)


app = FastAPI()
app.include_router(token.router)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]
