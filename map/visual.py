import matplotlib.pyplot as plt
import numpy as np


def visualize_forest(graph, path=None, start_id=None, goal_id=None):
    """
    Отрисовывает карту леса, типы местности и проложенный маршрут.
    """
    # 1. Вычисляем размеры нашей карты на основе координат вершин
    max_x = int(max(node.lon for node in graph.nodes.values()))
    max_y = int(max(node.lat for node in graph.nodes.values()))

    # 2. Создаем пустую матрицу (картинку) для RGB цветов
    # Размер +1, так как координаты начинаются с 0
    map_image = np.zeros((max_y + 1, max_x + 1, 3))

    # 3. Цветовая палитра для разных типов местности (RGB в формате от 0 до 1)
    colors = {
        "asphalt": (0.5, 0.5, 0.5),  # Серый
        "clear": (0.6, 0.9, 0.6),  # Светло-зеленый (полянка)
        "wood": (0.1, 0.5, 0.1),  # Темно-зеленый (густой лес)
        "dirt": (0.6, 0.4, 0.2),  # Коричневый (грунтовка)
        "dirt_trail": (0.6, 0.4, 0.2),  # Тоже коричневый
        "swamp": (0.3, 0.2, 0.4),  # Фиолетовый/болотный
        "unknown": (0.0, 0.0, 0.0)  # Черный (если забыли указать цвет)
    }

    # 4. Раскрашиваем каждый пиксель матрицы
    for node in graph.nodes.values():
        x, y = int(node.lon), int(node.lat)

        # Если точка вообще непроходима, красим её в темно-красный
        if not node.state.is_walkable:
            map_image[y, x] = (0.8, 0.1, 0.1)
        else:
            terrain = node.state.terrain_type
            map_image[y, x] = colors.get(terrain, colors["unknown"])

    # 5. Настраиваем график
    plt.figure(figsize=(10, 10))
    plt.title("Навигация по лесу (A* Algorithm)", fontsize=16)

    # Выводим матрицу как изображение
    # origin='lower' нужно, чтобы координаты (0,0) были в левом нижнем углу, как в математике
    plt.imshow(map_image, origin='lower')

    # 6. Отрисовываем маршрут, если он передан
    if path:
        path_x = [graph.get_node(node_id).lon for node_id in path]
        path_y = [graph.get_node(node_id).lat for node_id in path]
        # Рисуем яркую красную линию поверх карты
        plt.plot(path_x, path_y, color='red', linewidth=3, label='Найденный путь')

    # 7. Отмечаем старт и финиш
    if start_id and graph.get_node(start_id):
        start_node = graph.get_node(start_id)
        plt.scatter(start_node.lon, start_node.lat, color='cyan', marker='*', s=200, label='Старт', edgecolor='black',
                    zorder=5)

    if goal_id and graph.get_node(goal_id):
        goal_node = graph.get_node(goal_id)
        plt.scatter(goal_node.lon, goal_node.lat, color='yellow', marker='*', s=200, label='Финиш', edgecolor='black',
                    zorder=5)

    plt.legend(loc='upper right')
    plt.grid(False)  # Отключаем сетку, чтобы не мешала
    plt.show()