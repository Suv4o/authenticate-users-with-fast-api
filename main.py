import routes.token as token
from fastapi import Depends, FastAPI
from custom_types import CreateUser
from models import Users
from sqlalchemy.orm import Session
from config.database import get_db
from utils import (
    get_current_active_user,
)


app = FastAPI()
app.include_router(token.router)


@app.post("/user")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = Users(full_name=user.full_name, email=user.email, password=user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]
