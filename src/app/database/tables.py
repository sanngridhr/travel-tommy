from piccolo.table import Table
from piccolo.columns import M2M, UUID, Boolean, Date, ForeignKey, Integer, LazyTableReference, Varchar

class ProjectTable(Table):
    id = UUID(primary_key=True)
    name = Varchar(length=64, required=True)
    description = Varchar(null=True)
    start_date = Date(null=True)
    is_locked = Boolean(default=False)
    places = M2M(LazyTableReference("ProjectToPLace", module_path=__name__))

class PlaceTable(Table):
    id = UUID(primary_key=True)
    foreign_id = Integer(required=True)
    name = Varchar(length=64, required=True)
    notes = Varchar(null=True)
    is_visited = Boolean(default=False)
    projects = M2M(LazyTableReference("ProjectToPLace", module_path=__name__))

class ProjectToPlace(Table):
    project = ForeignKey(ProjectTable)
    place = ForeignKey(PlaceTable)