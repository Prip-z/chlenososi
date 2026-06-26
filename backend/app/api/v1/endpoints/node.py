from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.middleware import inject
from app.schema.base_schema import Blank
from app.schema.node_schema import FindNode, FindNodeResult, Node, UpsertNode
from app.services.node_service import NodeService

router = APIRouter(
    prefix="/nodes",
    tags=["nodes"],
)

@router.get("", response_model=FindNodeResult)
@inject
def get_nodes(
    find_query: FindNode = Depends(),
    service: NodeService = Depends(Provide[Container.node_service]),
):
    return service.get_list(find_query)


@router.get("/{node_id}", response_model=Node)
@inject
def get_node(
    node_id: int,
    service: NodeService = Depends(Provide[Container.node_service]),
):
    return service.get_by_id(node_id)


@router.post("", response_model=Node)
@inject
async def create_node(
    node: UpsertNode,
    service: NodeService = Depends(Provide[Container.node_service]),
):
    return service.add(node)


@router.patch("/{node_id}", response_model=Node)
@inject
def update_node(
    node_id: int,
    node: UpsertNode,
    service: NodeService = Depends(Provide[Container.node_service]),
):
    return service.patch(node_id, node)


@router.delete("/{node_id}", response_model=Blank)
@inject
def delete_node(
    node_id: int,
    service: NodeService = Depends(Provide[Container.node_service]),
):
    service.remove_by_id(node_id)
    return {}
