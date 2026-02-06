from piccolo.conf.apps import AppConfig

from app.database.tables import ProjectTable, PlaceTable


APP_CONFIG: AppConfig = AppConfig(
    app_name="app",
    migrations_folder_path="src/migrations",
    table_classes=[
        ProjectTable,
        PlaceTable,
    ],
)