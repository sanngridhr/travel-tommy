# Stack
+ Server - FastAPI
+ ORM - Piccolo
+ Database - SQLite
+ Package manager - Poetry


# Setup
## Envvars
Only DB_PATH needs to be set:
```ini
# .env
DB_PATH=static/db.sqlite3
```

## Installing dependencies
```sh
poetry install
```

## Migrations
```sh
# To create
poetry run piccolo migrations new app --auto
# To apply
poetry run piccolo migrations forwards app
```

## Running the app
```sh
poetry run uvicorn app.main:app --reload
```