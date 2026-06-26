import time
from random_forest import *
from a_star import *
from visual import *

# Генерируем карту 100 на 100 точек (это 10 000 узлов, приличный кусок леса)
print("Генерируем полигон...")
my_forest = generate_forest_polygon(100, 100)
print(f"Полигон готов. Узлов: {len(my_forest.nodes)}")

# Выбираем стартовую и конечную точки по диагонали через весь лес
start_point = "0_0"
goal_point = "99_99"

# Обязательно делаем их проходимыми, вдруг генератор закинул туда болото
my_forest.get_node(start_point).state.is_walkable = True
my_forest.get_node(goal_point).state.is_walkable = True

print(f"Ищем путь от {start_point} до {goal_point}...")

start_time = time.time()
path = bidirectional_a_star(my_forest, start_point, goal_point)
end_time = time.time()


if path:
    print(f"Путь найден! Длина: {len(path)}")
    # ВЫЗЫВАЕМ ОТРИСОВКУ:
    visualize_forest(my_forest, path, start_id=start_point, goal_id=goal_point)
else:
    print("Путь не найден.")
    # Можно отрисовать карту без пути, чтобы посмотреть, где мы застряли:
    visualize_forest(my_forest, start_id=start_point, goal_id=goal_point)