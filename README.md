# Stack
+ Server - FastAPI
+ ORM - Piccolo
+ Database - SQLite
+ Package manager - Poetry


# Setup
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