import routes.token as token
import routes.user as user
from fastapi import FastAPI

app = FastAPI()
app.include_router(token.router)
app.include_router(user.router)
