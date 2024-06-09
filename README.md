TODO:

-   DTO email validation
-   DTO password strong password validation
-   Create Database Fixtures
-   Clean and write the README.md

```bash
sh _run_dev.sh
```

or

```bash
poetry run uvicorn main:app --reload
```

or

```bash
poetry run fastapi dev main.py
```

Generate random key:

```bash
openssl rand -hex 32
```

### Docker

```bash
$ docker-compose up
```

## Scripts

Create Database Schema

```bash
$ sh _create_db_schema.sh
```

Drop Database Schema

```bash
$ sh _drop_db_schema.sh
```

### Create a migration

```bash
$ poetry run alembic revision --autogenerate -m "Migration name"
```

### Run migrations

```bash
$ poetry run alembic upgrade head
```

### Reverse migrations

```bash
$ poetry run alembic downgrade -1
```
