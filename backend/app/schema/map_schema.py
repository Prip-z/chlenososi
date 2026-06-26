from pydantic import BaseModel
from typing import List
from app.schema.base_schema import ModelBaseInfo

class BoundingBox(BaseModel):
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

class NodeResponse(ModelBaseInfo):
    map_id: int
    lat: float
    lon: float
    is_walkable: bool
    terrain_type: str

class EdgeResponse(ModelBaseInfo):
    source_id: int
    target_id: int
    weight: float

class MapAreaResponse(BaseModel):
    map_id: int
    pmtiles_url: str
    nodes: List[NodeResponse]
    edges: List[EdgeResponse]