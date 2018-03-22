# import library
import random
from collections import deque
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import matplotlib

"""
Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def UPA_graph(num_nodes, initial_node):
    """
    Create UPA_graph with num_nodes.
    """
    upa_graph = ER_graph(initial_node, 1)
    upa_trail = UPATrial(initial_node)
    for node in range(initial_node, num_nodes):
        neighbors = upa_trail.run_trial(initial_node)
        upa_graph[node] = neighbors
        for neighbor in neighbors:
            upa_graph[neighbor].add(node)

    return upa_graph


def ER_graph(num_nodes, p):
    """
    return a undirected complte graph of num_nodes nodes and adding edge to graph depends on p value
    """
    graph = {}
    if num_nodes > 0:
        for node in range(num_nodes):
            graph[node] = set([])

        for node_i in range(num_nodes):
            for node_j in range(node_i + 1, num_nodes):
                probality = random.random()
                if (probality < p):
                    graph[node_i].add(node_j)
                    graph[node_j].add(node_i)

    return graph


def random_order(ugraph):
    """
    return random order of ugraph  nodes.
    """
    r_order = []
    nodes = list(ugraph.keys())
    while len(nodes):
        removed_node = random.choice(nodes)
        r_order.append(removed_node)
        nodes.remove(removed_node)

    return r_order


def bfs_visited(ugraph, start_node):
    """
        Input : the undirected graph ugraph and the node start_node
        Output : the set consisting of all nodes that are visited by a breadth-first search that starts at start_node.
    """
    visited_nodes = set([start_node])
    queue = deque([start_node])
    while queue:
        node_u = queue.popleft()
        for node_v in ugraph[node_u]:
            if node_v not in visited_nodes:
                visited_nodes.add(node_v)
                queue.append(node_v)
    return visited_nodes


def cc_visited(ugraph):
    """
        Input : the undirected graph ugraph
        Output : A list of sets, where each set consists of all the nodes (and nothing else) in a connected component,
                and there is exactly one set in the list for each connected component in ugraph and nothing else.
    """
    cc_list = []
    remaining_nodes = set(ugraph.keys())
    while len(remaining_nodes):
        start_node = next(iter(remaining_nodes))
        cc_bfs = bfs_visited(ugraph, start_node)
        cc_list.append(cc_bfs)
        remaining_nodes = remaining_nodes.difference(cc_bfs)

    return cc_list


def largest_cc_size(ugraph):
    """
        Input : the undirected graph ugraph
        Output : the size (an integer) of the largest connected component in ugraph.
    """
    largest_cc = 0
    remaining_nodes = set(ugraph.keys())
    while len(remaining_nodes):
        start_node = next(iter(remaining_nodes))
        cc_bfs = bfs_visited(ugraph, start_node)
        largest_cc = max(largest_cc, len(cc_bfs))
        remaining_nodes = remaining_nodes.difference(cc_bfs)

    return largest_cc


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].discard(node)


def compute_resilience(ugraph, attack_order):
    """
        Input : the undirected graph ugraph, a list of nodes attack_order
        Output : return a list whose (k+1)th entry is the size of the largest connected component in the graph
                after the removal of the first k nodes in attack_order.
                The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """
    resilience = []
    largest_cc = largest_cc_size(ugraph)
    resilience.append(largest_cc)
    for attack_node in attack_order:
        ## remove attack_node from ugraph
        delete_node(ugraph, attack_node)
        largest_cc = largest_cc_size(ugraph)
        resilience.append(largest_cc)

    return resilience


NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print("Loaded graph with", len(graph_lines), "nodes")

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def print_graph(graph):
    for node in graph:
        print(node, graph[node])




#<=================================================>
# Question 1.
#
# network_graph = load_graph(NETWORK_URL)
# attack_order = random_order(network_graph)
# network_resilience = compute_resilience(network_graph, attack_order)
#
# p = 0.004
# num_node = 1239
# u_er_graph = ER_graph(num_node, p)
# attack_order = random_order(u_er_graph)
# u_er_resilience = compute_resilience(u_er_graph, attack_order)
#
# m = 2
# upa_graph = UPA_graph(num_node, m)
# attack_order = random_order(upa_graph)
# upa_resilience = compute_resilience(upa_graph, attack_order)
#
# x_val = [x for x in range(num_node+1)]
#
#
# matplotlib.rc('figure', figsize=(16, 8))
#
# # plot graph
# plt.plot(x_val, network_resilience, label = "Computer Network")
# plt.plot(x_val, u_er_resilience, label = "ER Graph, P = 0.004")
# plt.plot(x_val, upa_resilience, label = "UPA Graph, m = 2")
#
# # add label
# plt.legend()
# plt.xlabel("Number of node Removed")
# plt.ylabel("Size of largest connected component")
# plt.title("Comparison of graph resilience for random attack order")
# plt.grid(True)
#
# #plt.show()
# plt.savefig("resilience_random_q_1.png")

## question 2
"""
# All three graphs are resilient under random attack as the first 20% of
# their nodes are removed (unless the random order happens to remove a large
# number of high degree nodes, which is unlikely).
"""
def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


## question 3
def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)

    num_nodes = len(new_graph)
    degree_set = dict()
    for index in range(num_nodes):
        degree_set[index] = set([])
    for node in list(new_graph.keys()):
        degree = len(new_graph[node])
        degree_set[degree].add(node)

    node_order = []
    for degree in range(num_nodes-1,-1,-1):
        while (len(degree_set[degree])) :
            node = random.choice(list(degree_set[degree]))
            degree_set[degree].discard(node)
            for node_v in new_graph[node]:
                deg_node_v = len(new_graph[node_v])
                degree_set[deg_node_v].discard(node_v)
                degree_set[deg_node_v-1].add(node_v)
            node_order.append(node)
            delete_node(new_graph,node)

    return node_order

##

def q3():
    m = 5
    size = []
    run_time_slow = []
    run_time_fast = []
    for num_nodes in range(10, 1000,10):
        size.append(num_nodes)
        upa_graph = UPA_graph(num_nodes, m)
        start_time = time.time()
        attack_order = targeted_order(upa_graph)
        end_time  = time.time()
        time_taken_slow = end_time - start_time
        run_time_slow.append(time_taken_slow)
        ## fast
        time.sleep(0.002)
        start_time = time.time()
        attack_order = fast_targeted_order(upa_graph)
        end_time = time.time()
        time_taken_fast = end_time - start_time
        run_time_fast.append(time_taken_fast)

    matplotlib.rc('figure', figsize=(16, 8))

    print(len(size),len(run_time_slow),len(run_time_fast))
    # plot graph
    plt.plot(size, run_time_fast, label = "fast_targeted_order")
    plt.plot(size, run_time_slow, label = "targeted_order")

    # add label
    plt.legend()
    plt.xlabel("Size of UPA Graph m = 5")
    plt.ylabel("Running time in seconds")
    plt.title("Regular vs fast computation o targeted order")
    plt.grid(True)

    #plt.show()
    plt.savefig("targeted_order_q_3.png")

q3()

## Question 4



## Question 4
# network_graph = load_graph(NETWORK_URL)
# attack_order = targeted_order(network_graph)
# network_resilience = compute_resilience(network_graph, attack_order)
#
#
# p = 0.004
# num_node = 1239
# u_er_graph = ER_graph(num_node, p)
# attack_order = fast_targeted_order(u_er_graph)
# u_er_resilience = compute_resilience(u_er_graph, attack_order)
#
# m = 2
# upa_graph = UPA_graph(num_node, m)
# attack_order = targeted_order(upa_graph)
# upa_resilience = compute_resilience(upa_graph, attack_order)
#
# x_val = [x for x in range(num_node+1)]
#
#
# matplotlib.rc('figure', figsize=(16, 8))
#
# # plot graph
# plt.plot(x_val, network_resilience, label = "Computer Network")
# plt.plot(x_val, u_er_resilience, label = "ER Graph, P = 0.004")
# plt.plot(x_val, upa_resilience, label = "UPA Graph, m = 2")
# plt.plot(x_val, network_resilience2, label = "fast t o")
#
# # add label
# plt.legend()
# plt.xlabel("Number of node Removed")
# plt.ylabel("Size of largest connected component")
# plt.title("Comparison of graph resilience for random attack order")
# plt.grid(True)
#
# #plt.show()
# plt.savefig("resilience_targeted_q_4.png")
#

