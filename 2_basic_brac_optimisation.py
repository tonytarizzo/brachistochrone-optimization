import random

random.seed(42)
shape = [1,2,2,1]

def generate_graph(shape):
    graph = {}
    # Generate nodes and transitions
    for col in range(len(shape)):
        for pos in range(1, shape[col] + 1):
            # Node identifier, e.g., "1_1" for the first node in the first column
            node = f"{col+1}_{pos}"
            if col + 1 < len(shape):  # Check if not the last column
                # For each node, create transitions to nodes in the next column
                transitions = {}
                for next_pos in range(1, shape[col + 1] + 1):
                    next_node = f"{col+2}_{next_pos}"
                    # Assign a random cost to each transition
                    transitions[next_node] = random.randint(1, 9)
                graph[node] = transitions
            else:
                # Last column nodes have no outgoing transitions
                graph[node] = {}
    return graph

graph = generate_graph(shape)

final_state = f"{len(shape)}_1"
costs = {state: (float('inf'), None) for state in graph}
costs[final_state] = (0, None)

for state in reversed(list(graph.keys())[:-1]):
    for next_state, transition_cost in graph[state].items():
        total_cost = transition_cost + costs[next_state][0]
        if total_cost < costs[state][0]:
            costs[state] = (total_cost, next_state)

optimal_path = ['1_1']
current_state = '1_1'

while current_state != final_state:
    next_state = costs[current_state][1]
    optimal_path.append(next_state)
    current_state = next_state

print(optimal_path)

