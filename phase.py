import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time
import random

# Функция генерации случайного графа
def generate_graph(n) -> nx.DiGraph:
    # Генерация случайного графа с n вершинами
    G = nx.fast_gnp_random_graph(n, 0.2, seed=None, directed=False)

    # Убираем изолированные вершины
    # G.remove_nodes_from(list(nx.isolates(G)))
    if len(list(nx.isolates(G))) > 0:
        return generate_graph(n)

    # Проверяем, что граф связный, если нет - генерируем снова
    # if nx.is_weakly_connected(G) == False:
    #     return generate_graph(n)
    
    if nx.is_connected(G) == False:
        G = generate_graph(n)

    # Визуализируем граф
    pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=500, font_weight='bold')
    # plt.show()

    return G

# Класс для представления процесса
class Process:
    def __init__(self, name ,d):
        self.name = name
        self.Inc = {name}  # Initial set of included identifiers
        self.NInc = set()  # Initial set of non-included identifiers
        self.neighbors = set()  # Set of neighboring processes
        self.received_messages = {}
        self.m_count = 0
        self.predcessors = set()
        self.desendants = set()
        self.d = d
        self.closed = False
        self.m_sent = 0

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def add_predcessor(self, pred):
        self.predcessors.add(pred)

    def set_received_messages(self):
        for i in self.predcessors:
            self.received_messages[i] = 0

    def add_descendant(self,neighbor):
        self.desendants.add(neighbor)

    def receive_message(self, sender):
        """ Receive a message"""
        self.received_messages[sender] += 1
        self.m_count += 1


        if max(self.received_messages.values()) == min(self.received_messages.values()):
            if self.m_count // len(self.predcessors) == self.d:
                print(f"Node {self.name} closed")
                self.closed = True
            return True
        return False

    def send_message(self):
        """ Send the current sets to neighbors """
        if min(self.received_messages.values()) + 1 > self.m_sent and self.m_sent < self.d:
            self.m_sent += 1
            return self.name
        return None
    



# Класс для волнового алгоритма
class WaveAlgorithm:
    def __init__(self, processes):
        self.processes = {p.name: p for p in processes}
        self.names = [p.name for p in processes]
        self.steps = []

    def run(self):
        """ Run the wave algorithm until all processes have returned OK """
        qq =self.processes[self.names[0]]
        queue = deque([qq])  # Processes to be processed
        finished = set()
        n = 0 

        while queue and len(finished) < len(self.processes) and n < 200:
            n += 1
            current_process = queue.popleft()
            print("From " + str(current_process.name))

            name = current_process.send_message()
            if name is None:
                continue

            if current_process.closed == True:
                finished.add(current_process.name)
                print(f"Node {current_process.name} closed")

            print(f"Succecors of node {current_process.name}: {current_process.desendants}")
            # Update each of the neighbors
            for neighbor in current_process.desendants:
                if neighbor not in finished:
                    print("To " + str(neighbor))
                    self.processes[neighbor].receive_message(name)
                    if self.processes[neighbor].closed:
                        finished.add(neighbor)
                        for nn in self.processes[neighbor].neighbors:
                            if nn not in finished:
                                queue.append(self.processes[neighbor])
                    else:
                        queue.append(self.processes[neighbor])

            self.visualize_step()
            print("----------")
        
        self.visualize_step()
            

    def visualize_step(self):
            """ Visualize the current state of the processes """
            # graph = nx.DiGraph()
            for process in self.processes.values():
                # Draw each process and its sets
                label = f"{process.name} {list(process.received_messages.keys())}: {list(process.received_messages.values())}, sent: {process.m_sent}"
                print(label)
                # graph.add_node(process.name, label=label)
                # for neighbor in process.neighbors:
                #     graph.add_edge(process.name, neighbor)

if __name__ == "__main__":
    n = 7
    G = generate_graph(n)

    # Create processes based on the nodes
    processes = {node: Process(node, nx.diameter(G)) for node in G.nodes()}
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            processes[node].add_neighbor(neighbor)
        for neighbor in G.neighbors(node):
            processes[node].add_predcessor(neighbor)
        for neighbor in G.neighbors(node):
            processes[node].add_descendant(neighbor)
        processes[node].set_received_messages()

    # Run the wave algorithm
    algorithm = WaveAlgorithm(list(processes.values()))
    algorithm.run()
    nx.draw(G, with_labels=True)
    plt.show()
