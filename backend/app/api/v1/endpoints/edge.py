from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.middleware import inject
from app.schema.base_schema import Blank
from app.schema.edge_schema import Edge, FindEdge, FindEdgeResult, UpsertEdge
from app.services.edge_service import EdgeService

router = APIRouter(
    prefix="/edges",
    tags=["edges"],
)

@router.get("", response_model=FindEdgeResult)
@inject
def get_edges(
    find_query: FindEdge = Depends(),
    service: EdgeService = Depends(Provide[Container.edge_service]),
):
    return service.get_list(find_query)


@router.get("/{edge_id}", response_model=Edge)
@inject
def get_edge(
    edge_id: int,
    service: EdgeService = Depends(Provide[Container.edge_service]),
):
    return service.get_by_id(edge_id)


@router.post("", response_model=Edge)
@inject
def create_edge(
    edge: UpsertEdge,
    service: EdgeService = Depends(Provide[Container.edge_service]),
):
    return service.add(edge)


@router.patch("/{edge_id}", response_model=Edge)
@inject
def update_edge(
    edge_id: int,
    edge: UpsertEdge,
    service: EdgeService = Depends(Provide[Container.edge_service]),
):
    return service.patch(edge_id, edge)


@router.delete("/{edge_id}", response_model=Blank)
@inject
def delete_edge(
    edge_id: int,
    service: EdgeService = Depends(Provide[Container.edge_service]),
):
    service.remove_by_id(edge_id)
    return {}
