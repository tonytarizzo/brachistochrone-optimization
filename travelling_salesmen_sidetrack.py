import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random

# Generate a complete graph with weighted edges
def generate_graph(num_nodes):
    G = nx.complete_graph(num_nodes)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 10)  # Random weight for demonstration
    return G

# Calculate the length of the path
def path_length(G, path):
    return sum(G.edges[path[i], path[i + 1]]['weight'] for i in range(len(path) - 1))

# Brute-force solution to the TSP
def tsp_brute_force(G):
    nodes = list(G.nodes())
    min_path = None
    min_length = float('inf')

    # Generate all possible tours and check each one for the minimum length
    for permutation in itertools.permutations(nodes):
        # Make it a tour by returning to the start
        tour = list(permutation) + [permutation[0]]
        current_length = path_length(G, tour)
        if current_length < min_length:
            min_length = current_length
            min_path = tour

    return min_path, min_length

# Generate a graph and solve TSP
num_cities = 5
G = generate_graph(num_cities)
optimal_path, optimal_length = tsp_brute_force(G)

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

# Highlight the optimal path
edge_colors = ['black' if (optimal_path[i], optimal_path[i + 1]) not in zip(optimal_path, optimal_path[1:]) and
               (optimal_path[i + 1], optimal_path[i]) not in zip(optimal_path[1:], optimal_path) else 'red'
               for i in range(len(optimal_path) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=list(zip(optimal_path, optimal_path[1:])), edge_color=edge_colors)

plt.title(f'Optimal TSP path length: {optimal_length}')
plt.show()
