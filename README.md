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
