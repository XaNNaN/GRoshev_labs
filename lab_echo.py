import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from queue import Queue
from icecream import ic
import time

GRAPH_SIZE = 400
gr =plt.figure(0)


def generate_graph(n) -> nx.Graph:
    G = nx.empty_graph(0)
    G = nx.fast_gnp_random_graph(n, 0.38, seed=None, directed=False)
    
    G.remove_nodes_from(list(nx.isolates(G)))
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
    sented_to = ""
    global mrk_sent_counter
    for y in nei_to_sent:
        marker_sent_matrix[i, y] = 1
        sented_to += str(y) + ", "
        if marker_received_matrix[y].sum() == 0:
            parent_senter[y] = i
        marker_received_matrix[y, i] = 1
        if echo_sent[y] == 0:
            q.put(y)
            mrk_sent_counter = mrk_sent_counter +  1
    if GRAPH_SIZE  <= 100:
        ic("WAVE FROM " + str(i) + " TO " + sented_to[:-2])

def send_echo(i):
    if i == initiator:
        ic("FINISH")
        ic(marker_received_matrix[initiator][list(G.neighbors(initiator))])
        plt.figure(1)
        plt.plot( [i for i in range(iter_counter-1)], echo_to_draw, label='Echo')
        plt.plot([i for i in range(iter_counter-1)], wave_to_draw, label='Wave')
        plt.legend()
        plt.xlabel('Число итераций')
        plt.ylabel('Число маркеров')

        plt.figure(2)
        plt.plot( [i for i in range(iter_counter-1)], init_echo_rec_draw, label='Init echo get')
        plt.plot([i for i in range(iter_counter-1)], [initiator_nei for i in range(iter_counter - 1)], label='Init nei. count')
        plt.legend()
        plt.xlabel('Число итераций')
        plt.ylabel('Число маркеров')
        if GRAPH_SIZE >= 20:
            plt.close(gr)
        plt.show()
        exit(0)

    echo_sent[i] = 1
    global echo_sent_counter
    global init_echo_rec
    sented_to = ""
    all_nodes = marker_received_matrix[i]
    for y, parent in enumerate(all_nodes):
        if parent != 0: 
            sented_to += str(y) + ", "
            marker_sent_matrix[i, y] = 1
            marker_received_matrix[y, i] = 1
            if echo_sent[y] == 0:
                q.put(y)
                echo_sent_counter = echo_sent_counter +  1
            if y == initiator:
                init_echo_rec += 1
    if GRAPH_SIZE <= 20:
        ic("ECHO FROM " + str(i) + " TO " + sented_to[:-2])

start_time = time.time()
G = generate_graph(GRAPH_SIZE)
time_to_generate_graph = time.time() - start_time
ic(time_to_generate_graph)
marker_sent_matrix = np.zeros((G.__len__(), G.__len__())) 
marker_received_matrix = np.zeros((G.__len__(), G.__len__())) 
marker_sent = np.zeros(G.__len__())
parent_senter = np.zeros(G.__len__())
echo_sent = np.zeros(G.__len__())
mrk_sent_counter = int(0)
echo_sent_counter = int(0) 
iter_counter = int(0) 
echo_to_draw = []
wave_to_draw = []
init_echo_rec = 0
init_echo_rec_draw = []
q = Queue()


initiator = sample(list(G.nodes()), 1)[0]
initiator_nei = len(list(G.neighbors(initiator)))
ic(initiator)
send_marker(initiator)

while not q.empty():
    i = q.get() 
    
    iter_counter += 1

    if marker_sent[i] == 0:
        send_marker(i)

    check = np.array(G.neighbors(i))
    if marker_received_matrix[i].sum() == np.array(list(G.neighbors(i))).__len__() and echo_sent[i] == 0:
        send_echo(i)

    echo_to_draw.append(echo_sent_counter)
    wave_to_draw.append(mrk_sent_counter)
    init_echo_rec_draw.append(init_echo_rec)

print(marker_received_matrix)
print(marker_sent_matrix)
print(parent_senter)

if GRAPH_SIZE <= 20:
    plt.show()