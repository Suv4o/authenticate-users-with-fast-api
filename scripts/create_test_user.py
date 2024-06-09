import sys


sys.path.append("..")

import psycopg2
import logging
from config.logging import Logger
from config.env import get_env
from passlib.context import CryptContext
from datetime import datetime

env = get_env("../.env")

console = Logger("DATABASE").get()

conn = psycopg2.connect(
    host=env["POSTGRES_HOST"],
    port=env["POSTGRES_PORT"],
    database=env["POSTGRES_DB"],
    user=env["POSTGRES_USER"],
    password=env["POSTGRES_PASSWORD"],
)

cur = conn.cursor()

try:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    logging.getLogger("passlib").setLevel(logging.ERROR)

    full_name = "Test User"
    email = "test@user.com"
    password = pwd_context.hash("P@ssword1")
    disabled = False
    created_at = datetime.now()

    cur.execute(
        "INSERT INTO users (full_name, email, password, disabled, created_at) VALUES (%s, %s, %s, %s, %s)",
        (full_name, email, password, disabled, created_at),
    )
    console.info("Test user created successfully!")
except Exception as e:
    console.error(e)

conn.commit()

cur.close()
conn.close()
