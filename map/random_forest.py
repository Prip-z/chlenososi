import random
from graph import *


def generate_forest_polygon(width: int, height: int) -> Graph:
    forest = Graph()

    # 1. Создаем все вершины (узлы)
    for x in range(width):
        for y in range(height):
            node_id = f"{x}_{y}"

            # Немного рандома: 15% шанс на непроходимое болото
            is_walkable = True
            terrain = "dirt"
            if random.random() < 0.15:
                is_walkable = False
                terrain = "swamp"

            forest.add_node(node_id, lat=float(y), lon=float(x), is_walkable=is_walkable, terrain_type=terrain)

    # 2. Соединяем вершины (создаем ребра)
    for x in range(width):
        for y in range(height):
            current_id = f"{x}_{y}"
            if not forest.get_node(current_id).state.is_walkable:
                continue

            # Соединяем с соседями (право, низ, диагонали)
            # Мы проверяем только "вперед", т.к. add_edge двунаправленный
            neighbors = [
                (x + 1, y, 10.0),  # Право (вес 10)
                (x, y + 1, 10.0),  # Низ (вес 10)
                (x + 1, y + 1, 14.1),  # Диагональ право-низ (вес ~14.1 по Пифагору)
                (x + 1, y - 1, 14.1)  # Диагональ право-верх
            ]

            for nx, ny, weight in neighbors:
                if 0 <= nx < width and 0 <= ny < height:
                    target_id = f"{nx}_{ny}"
                    if forest.get_node(target_id).state.is_walkable:
                        # Добавим случайность в вес ребра (например, ухабы на дороге)
                        final_weight = weight * random.uniform(0.8, 1.2)
                        forest.add_edge(current_id, target_id, final_weight)

    return forest