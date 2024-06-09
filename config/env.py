from dotenv import dotenv_values

env = dotenv_values(".env")


def adjust_environment_variables(env):
    # Convert string to int
    env["ACCESS_TOKEN_EXPIRE_MINUTES"] = int(env.get("ACCESS_TOKEN_EXPIRE_MINUTES", 0))
    env["REFRESH_TOKEN_EXPIRE_DAYS"] = int(env.get("REFRESH_TOKEN_EXPIRE_DAYS", 0))

    # Set POSTGRES_URI
    env["POSTGRES_URI"] = (
        f"postgresql://{env.get('POSTGRES_USER')}:{env.get('POSTGRES_PASSWORD')}@{env.get('POSTGRES_HOST')}:{env.get('POSTGRES_PORT')}/{env.get('POSTGRES_DB')}"
    )


# Used anywhere we directly run python scripts. For example, scripts/drop_db_schema.py and scripts/create_db_schema.py
def get_env(file_path=".env"):
    env_values = dotenv_values(file_path)

    adjust_environment_variables(env_values)

    return env_values


adjust_environment_variables(env)
