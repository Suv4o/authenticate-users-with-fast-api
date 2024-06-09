# Prerequisites

-   `pyenv` - It assists in managing Python versions. This project was created using Python 3.12.3
-   `poetry` - For managing dependencies
-   Docker - We are using `docker-compose` to run our PostgreSQL database
-   Use the VS Code - Black Formatter Extension along with the other recommended extensions found in the `.vscode/extensions.json` file
-   TablePlus - A modern, native, and user-friendly GUI tool for relational databases - (https://tableplus.com/)

# Environment Variables

```bash
cp .env.example .env
```

Generate a random `SECRET_KEY` using the following command line

```bash
openssl rand -hex 32
```

# Getting Started

## Run the local server on port `http://127.0.0.1:8000`

```bash
$ sh _run_dev.sh
```

or

```bash
$ poetry run uvicorn main:app --reload
```

## Run a local PostgreSQL database

```bash
$ docker-compose up
```

## Export dependencies to the `requirements.txt` file

```bash
$ sh _export_requirements.sh
```

# Database Migrations

## Create Database Schema

```bash
$ sh _create_db_schema.sh

```

## Drop Database Schema

```bash
$ sh _drop_db_schema.sh

```

## Create a migration

```bash
$ sh _new_migration.sh new_migration_name

```

## Run migrations

```bash
$ sh _migration_up.sh

```

## Reverse migrations

```bash
$ sh _migration_down.sh

```

## Create a new test user

Use this to create a test user once the migration is complete
