from piccolo.table import Table
from piccolo.columns import UUID, Boolean, Date, ForeignKey, OnDelete, Varchar

from app.database.piccolo_conf import DB


class BaseTable(Table):
    db = DB


class ProjectTable(BaseTable):
    id = UUID(primary_key=True)
    name = Varchar(length=64, required=True)
    description = Varchar(null=True)
    start_date = Date(null=True)


class PlaceTable(BaseTable):
    id = UUID(primary_key=True)
    title = Varchar(length=64, required=True)
    notes = Varchar(null=True)
    is_visited = Boolean(default=False, required=True)
    project = ForeignKey(ProjectTable, on_delete=OnDelete.cascade)
