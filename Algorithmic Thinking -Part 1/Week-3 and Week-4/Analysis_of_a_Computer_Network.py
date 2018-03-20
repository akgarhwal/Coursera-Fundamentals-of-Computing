# import library
import random
from collections import deque


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
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors



def UPA_graph(num_nodes,initial_node):
    """
    Create UPA_graph with num_nodes.
    """
    upa_graph = ER_graph(initial_node,1)
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
            for node_j in range(node_i+1,num_nodes):
                probality = random.random()
                if (probality < p) :
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
        cc_bfs = bfs_visited(ugraph,start_node)
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
        cc_bfs = bfs_visited(ugraph,start_node)
        largest_cc = max(largest_cc,len(cc_bfs))
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



def print_graph(graph):
    for node in graph:
        print(node, graph[node])


## test ER_graph

# u_er_graph = ER_graph(1239,0.004)
# attack_order = random_order(u_er_graph)

# u_er_resilience = compute_resilience(u_er_graph, attack_order)

# print(u_er_resilience)

# x_val = [x for x in range(1240)]
# print()
# print(x_val)



# for node in er_graph:
#     print(node,er_graph[node])
# print()



upa_graph = UPA_graph(1239,2)
#print_graph(upa_graph)
attack_order = random_order(upa_graph)
#print(attack_order)

upa_resilience = compute_resilience(upa_graph, attack_order)

print(upa_resilience)

x_val = [x for x in range(1240)]
print()
print(x_val)

#for node in graph:
#     #print(node, graph[node])

# print()



#print(random_order(er_graph))
