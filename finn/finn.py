import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

# Функция генерации случайного графа
def generate_graph(n) -> nx.DiGraph:
    # Генерация случайного графа с n вершинами
    G = nx.fast_gnp_random_graph(n, 0.2, seed=None, directed=True)

    # Убираем изолированные вершины
    G.remove_nodes_from(list(nx.isolates(G)))

    # Проверяем, что граф связный, если нет - генерируем снова
    if nx.is_weakly_connected(G) == False:
        return generate_graph(n)
    
    # Визуализируем граф
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=500, font_weight='bold')
    plt.show()

    return G

# Класс для представления процесса
class Process:
    def __init__(self, name):
        self.name = name
        self.Inc = {name}  # Initial set of included identifiers
        self.NInc = set()  # Initial set of non-included identifiers
        self.neighbors = set()  # Set of neighboring processes
        self.received_messages = 0
        self.predcessors = set()
        self.desendants = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def add_predcessor(self, pred):
        self.predcessors.add(pred)

    def add_descendant(self,neighbor):
        self.desendants.add(neighbor)

    def receive_message(self, Inc, NInc):
        """ Receive a message, update Inc and NInc sets, and return if ready """
        self.Inc.update(Inc)
        self.NInc.update(NInc)
        self.received_messages += 1
        print(f"Node {self.name} Inc: {self.Inc}")
        print(f"Node {self.name} NInc: {self.NInc}")

        # Условие для добавления в NInc(s) после получения всех сообщений от входящих соседей
        if self.received_messages == len(self.predcessors) + 1:
            self.NInc.add(self.name)  # Добавляем себя в NInc
        if self.Inc == self.NInc:
            print(f"Node {self.name} closed")
            return True
        return False

    def send_message(self):
        """ Send the current sets to neighbors """
        return self.Inc, self.NInc


# Класс для волнового алгоритма
class WaveAlgorithm:
    def __init__(self, processes):
        self.processes = {p.name: p for p in processes}
        self.steps = []

    def run(self):
        """ Run the wave algorithm until all processes have returned OK """
        queue = deque(self.processes.values())  # Processes to be processed
        finished = set()

        while queue and len(finished) < len(self.processes):
            # Iterate over all processes in the queue
            current_process = queue.popleft()
            print("From " + str(current_process.name))

            # Send messages to neighbors
            Inc, NInc = current_process.send_message()

            if current_process.receive_message(Inc, NInc):
                finished.add(current_process.name)

            print(f"Succecors of node {current_process.name}: {current_process.desendants}")
            # Update each of the neighbors
            for neighbor in current_process.desendants:
                if neighbor not in finished:
                    print("To " + str(neighbor))
                    if self.processes[neighbor].receive_message(Inc, NInc):
                        finished.add(neighbor)
                    else:
                        queue.append(self.processes[neighbor])

            # If current process has received all messages, it is ready


            # Record the step
            self.steps.append(self.visualize_step())
            print("----------")
            # Delay to simulate time step (for visualization purposes)
            # time.sleep()

    def visualize_step(self):
        """ Visualize the current state of the processes """
        graph = nx.DiGraph()
        for process in self.processes.values():
            # Draw each process and its sets
            label = f"{process.name} Inc: {sorted(process.Inc)} NInc: {sorted(process.NInc)}"
            print(label)
            graph.add_node(process.name, label=label)
            for neighbor in process.neighbors:
                graph.add_edge(process.name, neighbor)

        # Visualize the current state of the graph
        # pos = nx.spring_layout(graph)
        # nx.draw_networkx(graph, pos, with_labels=False, node_color='lightblue', font_size=10, node_size=500, font_weight='bold')

        # node_labels = nx.get_node_attributes(graph, 'label')
        # nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=10, font_color='black')

        # plt.show()


# Example usage
if __name__ == "__main__":
    # Generate random graph with 6 nodes
    n = 8
    G = generate_graph(n)

    # Create processes based on the nodes
    processes = {node: Process(node) for node in G.nodes()}
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            processes[node].add_neighbor(neighbor)
        for neighbor in G.predecessors(node):
            processes[node].add_predcessor(neighbor)
        for neighbor in G.successors(node):
            processes[node].add_descendant(neighbor)

    # Run the wave algorithm
    algorithm = WaveAlgorithm(list(processes.values()))
    algorithm.run()
    nx.draw(G, with_labels=True)
    plt.show()
