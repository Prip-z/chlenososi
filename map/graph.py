from dataclasses import dataclass, field
from typing import Dict, List, Optional


# 1. Состояние вершины
# Выносим отдельно, чтобы было удобно менять статусы (например, "затопило")
# без изменения координат.
@dataclass
class NodeState:
    is_walkable: bool = True
    terrain_type: str = "dirt_trail"
    # Сюда потом можно добавить множитель сложности:
    # difficulty_multiplier: float = 1.0


# 2. Ребро (Связь)
# Хранит только ID куда идем и сколько это стоит.
@dataclass
class Edge:
    target_id: str
    weight: float


# 3. Сама вершина (Узел)
@dataclass
class Node:
    node_id: str
    lat: float
    lon: float
    state: NodeState
    # Используем default_factory, чтобы у каждого узла был свой независимый список
    edges: List[Edge] = field(default_factory=list)

    def add_edge(self, target_id: str, weight: float):
        """Добавляет связь с другой вершиной."""
        # Проверка от дубликатов (опционально, но полезно)
        if not any(edge.target_id == target_id for edge in self.edges):
            self.edges.append(Edge(target_id, weight))


# 4. Класс Графа (Управляет всем лесом)
class Graph:
    def __init__(self):
        # Хеш-таблица (словарь) для мгновенного доступа O(1) по ID
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node_id: str, lat: float, lon: float, is_walkable: bool = True,
                 terrain_type: str = "dirt_trail") -> Node:
        """Создает и регистрирует новую точку на карте."""
        if node_id in self.nodes:
            raise ValueError(f"Вершина с ID {node_id} уже существует!")

        state = NodeState(is_walkable=is_walkable, terrain_type=terrain_type)
        new_node = Node(node_id=node_id, lat=lat, lon=lon, state=state)
        self.nodes[node_id] = new_node
        return new_node

    def add_edge(self, from_id: str, to_id: str, weight: float, bidirectional: bool = True):
        """
        Соединяет две точки.
        bidirectional=True означает, что по тропинке можно пройти в обе стороны.
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            raise ValueError("Обе вершины должны существовать в графе перед добавлением ребра.")

        self.nodes[from_id].add_edge(to_id, weight)

        if bidirectional:
            self.nodes[to_id].add_edge(from_id, weight)

    def get_node(self, node_id: str) -> Optional[Node]:
        """Безопасное получение узла."""
        return self.nodes.get(node_id)

    def get_walkable_neighbors(self, node_id: str) -> List[Edge]:
        """
        Главный метод для алгоритма A*.
        Возвращает куда можно пойти, отсекая непроходимые пути.
        """
        node = self.get_node(node_id)
        if not node or not node.state.is_walkable:
            return []

        valid_edges = []
        for edge in node.edges:
            target_node = self.get_node(edge.target_id)
            # Добавляем в соседи только если целевая точка проходима
            if target_node and target_node.state.is_walkable:
                valid_edges.append(edge)

        return valid_edges