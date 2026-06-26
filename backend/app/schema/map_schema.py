from typing import List, Optional

from pydantic import BaseModel

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BoundingBox(BaseModel):
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float


class MapBase(BaseModel):
    name: str
    pmtiles_url: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class Map(ModelBaseInfo, MapBase):
    ...


class FindMap(FindBase, MapBase, metaclass=AllOptional):
    ...


class UpsertMap(MapBase, metaclass=AllOptional):
    ...


class FindMapResult(BaseModel):
    founds: Optional[List[Map]]
    search_options: Optional[SearchOptions]


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