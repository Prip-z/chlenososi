from contextlib import AbstractContextManager
from typing import Any, Callable

from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from app.model.map_graph import Node
from app.repository.base_repository import BaseRepository


class NodeRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Node)

    def create(self, schema: Any):
        data = schema.dict(exclude_none=True)
        lat = data.pop("lat", None)
        lon = data.pop("lon", None)
        geom = data.pop("geom", None) if "geom" in data else None
        if lat is not None and lon is not None:
            data["geom"] = WKTElement(f"POINT({lon} {lat})", srid=4326)
        elif geom is not None and isinstance(geom, str):
            data["geom"] = WKTElement(geom, srid=4326)

        query = self.model(**data)
        with self.session_factory() as session:
            session.add(query)
            session.commit()
            session.refresh(query)
        return query

    def update(self, id: int, schema: Any):
        data = schema.dict(exclude_none=True)
        lat = data.pop("lat", None)
        lon = data.pop("lon", None)
        geom = data.pop("geom", None) if "geom" in data else None
        if lat is not None and lon is not None:
            data["geom"] = WKTElement(f"POINT({lon} {lat})", srid=4326)
        elif geom is not None and isinstance(geom, str):
            data["geom"] = WKTElement(geom, srid=4326)

        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(data)
            session.commit()
            return self.read_by_id(id)
