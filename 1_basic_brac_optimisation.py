graph = {
    'A': {'B': 7},
    'B': {'D': 2, 'E': 1},
    'C': {'E': 3},
    'D': {'F': 8},
    'E': {'F': 6},
    'F': {}
}

costs = {state: (float('inf'), None) for state in graph}
costs['F'] = (0, None)

for state in reversed(list(graph.keys())[:-1]):
    for next_state, transition_cost in graph[state].items():
        total_cost = transition_cost + costs[next_state][0]
        if total_cost < costs[state][0]:
            costs[state] = (total_cost, next_state)

optimal_path = ['A']
current_state = 'A'

while current_state != 'F':
    next_state = costs[current_state][1]
    optimal_path.append(next_state)
    current_state = next_state

print(optimal_path, costs)