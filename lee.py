import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Функция генерации случайного графа
def generate_graph(n) -> nx.DiGraph:
    # Генерация случайного графа с n вершинами
    G = nx.fast_gnp_random_graph(n, 0.2, seed=None, directed=False)

    # Убираем изолированные вершины
    if len(list(nx.isolates(G))) > 0:
        return generate_graph(n)

    # Проверяем, что граф связный, если нет - генерируем снова
    if nx.is_connected(G) == False:
        G = generate_graph(n)

    # Визуализируем граф
    pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=500, font_weight='bold')
    # plt.show()

    return G

# Алгоритм Ли для поиска кратчайших путей
def lee_algorithm(graph, start):
    """
    Алгоритм Ли для поиска кратчайших путей в графе с положительными целыми весами рёбер.
    
    graph - это словарь, где ключи — вершины, а значения — список кортежей (сосед, вес ребра).
    start - начальная вершина для поиска.
    """
    # Инициализация
    distances = {node: float('inf') for node in graph}  # Все расстояния бесконечны
    distances[start] = 0  # Расстояние до начальной вершины равно 0
    queue = deque([start])  # Очередь для обработки вершин

    while queue:
        current_node = queue.popleft()  # Извлекаем вершину из очереди

        # Обрабатываем всех соседей текущей вершины
        for neighbor in graph[current_node]:
            # Если найден более короткий путь, обновляем расстояние
            if distances[neighbor] > distances[current_node] + 1:  # Веса рёбер равны 1
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)  # Добавляем соседа в очередь для дальнейшей обработки

    return distances

# Пример использования

# Генерируем случайный граф с 10 вершинами
n = 10
G = generate_graph(n)

# Преобразуем граф в формат, удобный для алгоритма Ли
# Для этого создадим словарь, где ключи - вершины, а значения - список соседей
graph_dict = {node: [neighbor for neighbor in G.neighbors(node)] for node in G.nodes}

# Запуск алгоритма Ли от вершины '0' (если такая существует)
start_node = 0

if start_node in graph_dict:
    shortest_paths = lee_algorithm(graph_dict, start_node)

    # Вывод результатов
    print(f"Кратчайшие расстояния от вершины {start_node}:")
    for node, distance in shortest_paths.items():
        print(f"{node}: {distance}")
else:
    print(f"Вершина {start_node} не существует в графе.")


pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=500, font_weight='bold')
plt.show()
