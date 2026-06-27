from app.repository.node_repository import NodeRepository
from app.services.base_service import BaseService
from app.schema.node_schema import UpsertNode
class NodeService(BaseService):
    def __init__(self, node_repository: NodeRepository):
        self.node_repository = node_repository
        super().__init__(node_repository)

    def add(self, node_data: UpsertNode):
        data = node_data.dict(exclude_none=True)
        data.pop("id", None)
        clean_node = UpsertNode(**data)
        
        return self.node_repository.create(clean_node)