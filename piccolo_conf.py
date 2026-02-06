from piccolo.conf.apps import AppRegistry
from app.database.piccolo_conf import DB as DB


APP_REGISTRY: AppRegistry = AppRegistry(
    apps=["app.piccolo_app"],
)
