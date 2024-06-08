from dotenv import dotenv_values

env = dotenv_values(".env")

# Convert string to int
env["ACCESS_TOKEN_EXPIRE_MINUTES"] = int(env["ACCESS_TOKEN_EXPIRE_MINUTES"])
env["REFRESH_TOKEN_EXPIRE_DAYS"] = int(env["REFRESH_TOKEN_EXPIRE_DAYS"])
