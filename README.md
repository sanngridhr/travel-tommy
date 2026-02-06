# Stack
+ Server - FastAPI
+ ORM - Piccolo
+ Database - SQLite
+ Package manager - Poetry

# Assumptions
## Projects are isolated
Every project belongs to one user and places are not shared between projects.
## Component-based frontend
Frontend is build around components (React, Angular etc.) and only strictly needed component data is shared and received to improve performance and ease of development.

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

## Swagger docs
Available on http://0.0.0.0:8000/docs
