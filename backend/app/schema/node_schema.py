from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class NodeBase(BaseModel):
    map_id: int
    lat: Optional[float] = None
    lon: Optional[float] = None
    is_walkable: bool = True
    terrain_type: str = "dirt_trail"

    class Config:
        orm_mode = True


class Node(ModelBaseInfo, NodeBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FindNode(FindBase, NodeBase, metaclass=AllOptional):
    ...


class UpsertNode(NodeBase, metaclass=AllOptional):
    ...


class FindNodeResult(BaseModel):
    founds: Optional[List[Node]]
    search_options: Optional[SearchOptions]
