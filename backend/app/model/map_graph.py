from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class Map(Base):
    __tablename__ = "maps"  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pmtiles_url = Column(String, nullable=False)
    description = Column(String, default=None, nullable=True)


class Node(Base):
    __tablename__ = "nodes" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_id = Column(Integer, ForeignKey("maps.id"), index=True)
    geom = Column(Geometry("POINT", srid=4326))
    is_walkable = Column(Boolean, default=True)
    terrain_type = Column(String, default="dirt_trail")


class Edge(Base):
    __tablename__ = "edges"
    
    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("maps.id"), index=True)
    source_id = Column(String(50), ForeignKey("nodes.id"), index=True)
    target_id = Column(String(50), ForeignKey("nodes.id"), index=True)
    weight = Column(Float, nullable=False)