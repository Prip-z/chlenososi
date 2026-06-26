from typing import Any
from sqlmodel import Field
from sqlalchemy import Column
from geoalchemy2 import Geometry
from app.model.base_model import BaseModel

class Map(BaseModel, table=True):
    __tablename__ = "maps"  
    name: str = Field(index=True)
    pmtiles_url: str = Field()
    description: str = Field(default=None, nullable=True)

class Node(BaseModel, table=True):
    __tablename__ = "nodes" 

    map_id: int = Field(foreign_key="maps.id", index=True) # Имя таблицы изменилось на maps
    geom: Any = Field(sa_column=Column(Geometry("POINT", srid=4326)))
    is_walkable: bool = Field(default=True)
    terrain_type: str = Field(default="dirt_trail")

class Edge(BaseModel, table=True):
    __tablename__ = "edges"
    
    map_id: int = Field(foreign_key="maps.id", index=True)
    source_id: int = Field(foreign_key="nodes.id", index=True)
    target_id: int = Field(foreign_key="nodes.id", index=True)
    weight: float = Field()