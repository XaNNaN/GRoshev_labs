import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from queue import Queue

def generate_graph(n) -> nx.Graph:
    G = nx.empty_graph(0)
    G = nx.fast_gnp_random_graph(n, 0.38, seed=None, directed=False)
    
    # G.remove_nodes_from(list(nx.isolates(G)))
    pos = nx.arf_layout(G)

    if nx.is_connected(G) == False:
        G = generate_graph(n)
    else:
        nx.draw(G, pos=pos, with_labels=True)
    return G 

def send_marker(i):
    marker_sent[i] = 1
    nei_matrix = marker_sent_matrix[list(G.neighbors(i)), i].astype(int)
    nei_to_sent = np.array(list(G.neighbors(i)))[~nei_matrix.astype(bool)]
    for y in nei_to_sent:
        marker_sent_matrix[i, y] = 1
        if marker_received_matrix[y].sum() == 0:
            parent_senter[y] = i
        marker_received_matrix[y, i] = 1
        if echo_sent[y] == 0:
            q.put(y)

def send_echo(i):
    if i == initiator:
        print("FINISH")
        exit(0)
    echo_sent[i] = 1
    all_nodes = marker_received_matrix[i]
    for y, parent in enumerate(all_nodes):
        if parent != 0: 
            marker_sent_matrix[i, y] = 1
            marker_received_matrix[y, i] = 1
            if echo_sent[y] == 0:
                q.put(y)


G = generate_graph(1000)
marker_sent_matrix = np.zeros((G.__len__(), G.__len__())) 
marker_received_matrix = np.zeros((G.__len__(), G.__len__())) 
marker_sent = np.zeros(G.__len__())
parent_senter = np.zeros(G.__len__())
echo_sent = np.zeros(G.__len__())
q = Queue()

initiator = sample(list(G.nodes()), 1)[0]
print(initiator)
send_marker(initiator)

while not q.empty():
    i = q.get() 

    if marker_sent[i] == 0:
        send_marker(i)

    check = np.array(G.neighbors(i))
    if marker_received_matrix[i].sum() == np.array(list(G.neighbors(i))).__len__() and echo_sent[i] == 0:
        print("Send ECHO " +  str(i))
        send_echo(i)

print(marker_received_matrix)
print(marker_sent_matrix)
print(parent_senter)

plt.show()