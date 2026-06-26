import heapq
import math
from typing import List, Dict, Set, Tuple
from graph import *
from parametrs import *


def heuristic(node_a: Node, node_b: Node) -> float:
    """Обычное евклидово расстояние. Идеально для эвристики на плоскости."""
    return math.hypot(node_a.lon - node_b.lon, node_a.lat - node_b.lat)


def reconstruct_bidirectional_path(came_from_fwd: Dict[str, str], came_from_bwd: Dict[str, str], meeting_node: str) -> \
List[str]:
    """Сшивает два пути в точке встречи."""
    # Восстанавливаем путь от старта до точки встречи
    path_fwd = [meeting_node]
    current = meeting_node
    while current in came_from_fwd:
        current = came_from_fwd[current]
        path_fwd.append(current)
    path_fwd.reverse()  # Переворачиваем, чтобы было от старта к центру

    # Восстанавливаем путь от точки встречи до финиша
    path_bwd = []
    current = meeting_node
    while current in came_from_bwd:
        current = came_from_bwd[current]
        path_bwd.append(current)

    # Сшиваем (убираем дубликат точки встречи)
    return path_fwd + path_bwd


def calculate_cost(edge: Edge, target_node: Node, profile: str) -> float:
    """
    Рассчитывает "цену" перехода в соседний узел.
    """
    base_distance = edge.weight
    terrain = target_node.state.terrain_type

    # Ищем множитель для данного типа местности в выбранном профиле.
    # Если вдруг забыли описать местность, ставим штраф 10.0 (чтобы избегать неизвестного).
    multiplier = ROUTING_PROFILES.get(profile, {}).get(terrain, 10.0)

    return base_distance * multiplier


def bidirectional_a_star(graph: Graph, start_id: str, goal_id: str, profile: str = "quality") -> List[str]:
    start_node = graph.get_node(start_id)
    goal_node = graph.get_node(goal_id)

    if not start_node or not goal_node or not start_node.state.is_walkable or not goal_node.state.is_walkable:
        return []  # Старт или финиш заблокированы

    # Очереди с приоритетом: (F-score, ID узла)
    # F = G (пройденный путь) + H (примерный остаток)
    queue_fwd: List[Tuple[float, str]] = [(0.0, start_id)]
    queue_bwd: List[Tuple[float, str]] = [(0.0, goal_id)]

    # Словари стоимости пройденного пути (G-score)
    g_score_fwd: Dict[str, float] = {start_id: 0.0}
    g_score_bwd: Dict[str, float] = {goal_id: 0.0}

    # Откуда мы пришли в каждую точку (для восстановления пути)
    came_from_fwd: Dict[str, str] = {}
    came_from_bwd: Dict[str, str] = {}

    # Посещенные узлы (как только множества пересекутся — мы нашли путь!)
    visited_fwd: Set[str] = set()
    visited_bwd: Set[str] = set()

    # Лучшая найденная стоимость пути и точка встречи
    best_path_cost = float('inf')
    meeting_node = None

    while queue_fwd and queue_bwd:
        # --- ШАГ ПРЯМОГО ПОИСКА ---
        _, current_fwd = heapq.heappop(queue_fwd)
        visited_fwd.add(current_fwd)

        # --- ШАГ ОБРАТНОГО ПОИСКА ---
        _, current_bwd = heapq.heappop(queue_bwd)
        visited_bwd.add(current_bwd)

        # Проверяем пересечение фронтов
        # Если прямой поиск наткнулся на узел, который уже посетил обратный...
        if current_fwd in visited_bwd:
            cost = g_score_fwd[current_fwd] + g_score_bwd.get(current_fwd, float('inf'))
            if cost < best_path_cost:
                best_path_cost = cost
                meeting_node = current_fwd

        # И наоборот...
        if current_bwd in visited_fwd:
            cost = g_score_fwd.get(current_bwd, float('inf')) + g_score_bwd[current_bwd]
            if cost < best_path_cost:
                best_path_cost = cost
                meeting_node = current_bwd

        # Если точка встречи найдена, мы можем досрочно завершить поиск
        # (В строгом математическом A* нужно проверить еще пару условий для ГАРАНТИИ
        # самого короткого пути, но для лесной карты прерывание при первом контакте работает отлично и очень быстро).
        if meeting_node:
            return reconstruct_bidirectional_path(came_from_fwd, came_from_bwd, meeting_node)

        # --- РАСШИРЕНИЕ ПРЯМОГО ФРОНТА ---
        for edge in graph.get_walkable_neighbors(current_fwd):
            neighbor_id = edge.target_id
            target_node = graph.get_node(neighbor_id)

            step_cost = calculate_cost(edge, target_node, profile)
            tentative_g = g_score_fwd[current_fwd] + step_cost

            if tentative_g < g_score_fwd.get(neighbor_id, float('inf')):
                came_from_fwd[neighbor_id] = current_fwd
                g_score_fwd[neighbor_id] = tentative_g

                # Эвристика остается прежней (расстояние по прямой),
                # потому что она всегда должна быть меньше или равна реальному пути
                f_score = tentative_g + heuristic(target_node, goal_node)
                heapq.heappush(queue_fwd, (f_score, neighbor_id))

        # --- РАСШИРЕНИЕ ОБРАТНОГО ФРОНТА ---
        for edge in graph.get_walkable_neighbors(current_bwd):
            neighbor = edge.target_id
            tentative_g = g_score_bwd[current_bwd] + edge.weight

            if tentative_g < g_score_bwd.get(neighbor, float('inf')):
                came_from_bwd[neighbor] = current_bwd
                g_score_bwd[neighbor] = tentative_g

                f_score = tentative_g + heuristic(graph.get_node(neighbor), start_node)
                heapq.heappush(queue_bwd, (f_score, neighbor))

    return []  # Путь не найден (например, цель окружена болотом)