from typing import List, Optional

from pydantic import BaseModel

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class EdgeBase(BaseModel):
    map_id: int
    source_id: int
    target_id: int
    weight: float

    class Config:
        orm_mode = True


class Edge(ModelBaseInfo, EdgeBase):
    ...


class FindEdge(FindBase, EdgeBase, metaclass=AllOptional):
    ...


class UpsertEdge(EdgeBase, metaclass=AllOptional):
    ...


class FindEdgeResult(BaseModel):
    founds: Optional[List[Edge]]
    search_options: Optional[SearchOptions]
