""" Assignment Week-4
"""
from collections import deque

GRAPH6 = {1: set([2, 5]),
          2: set([1, 7]),
          3: set([4, 6, 9]),
          4: set([3, 6, 9]),
          5: set([1, 7]),
          6: set([3, 4, 9]),
          7: set([2, 5]),
          9: set([3, 4, 6])}


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
        ugraph.pop(attack_node, None)
        for node in ugraph.keys():
            ugraph[node].discard(attack_node)
            
        largest_cc = largest_cc_size(ugraph)
        resilience.append(largest_cc)
    
    return resilience


