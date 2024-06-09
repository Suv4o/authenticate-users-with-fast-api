import sys

sys.path.append("../")

import psycopg2

from config.logging import Logger
from config.env import get_env

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
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
    console.info("Dropped schema public")
except Exception as e:
    pass
    console.error(e)

conn.commit()

cur.close()
conn.close()
