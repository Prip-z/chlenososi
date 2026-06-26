from app.repository.node_repository import NodeRepository
from app.services.base_service import BaseService
from app.schema.node_schema import UpsertNode
class NodeService(BaseService):
    def __init__(self, node_repository: NodeRepository):
        self.node_repository = node_repository
        super().__init__(node_repository)

    def add(self, node_data: UpsertNode):
        # 1. Принудительно выкидываем ID, если он там есть, 
        # чтобы база сама его сгенерила (убирает FlushError)
        data = node_data.dict(exclude_none=True)
        data.pop("id", None)
        
        # 2. Создаем Pydantic-объект на лету из чистого словаря.
        # Теперь репозиторий получит Pydantic-объект, у него будет .dict(), 
        # и все довольны. Никаких AttributeError.
        clean_node = UpsertNode(**data)
        
        return self.node_repository.create(clean_node)