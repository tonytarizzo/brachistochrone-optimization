import random

random.seed(42)

start_x=0
start_y=50
end_x=25
end_y=20
starting_velocity = 0

g = 9.81

def calculate_shape(start_x, start_y, end_x, end_y, starting_velocity):
    x_range = abs(end_x - start_x + 1)
    y_range = round((start_y - end_y)*1.5)
    shape = [y_range] * x_range
    return shape

def calculate_cost(ax, ay, bx, by, vx):
    h_diff = ay - by
    effective_h_diff = h_diff if h_diff > 0 else 0
    vx = (2 * g * effective_h_diff)**0.5  # Ball can't go upwards without initial velocity
    # Distance from A to X
    s_ax = ((ax - bx)**2 + (ay - by)**2)**0.5
    # Average velocity from A to X
    v_ax = (vx + 0) / 2  # Initial velocity (v_A) is 0 because the ball starts from rest
    # Time taken to travel from A to X (cost), assuming v_ax is not zero to avoid division by zero
    time = s_ax / v_ax if v_ax != 0 else float('inf')
    return time

def generate_graph_physical(shape, start_x, start_y, end_x, end_y, starting_velocity):
    graph = {}
    current_velocity = starting_velocity
    # Adjust node generation to reflect x,y positions
    for col in range(len(shape)):
        x_position = start_x + col
        y_position = start_y  # Starting y position for the top node in each column
        for pos in range(shape[col]):
            y_position = start_y - pos
            node = f"{x_position}_{y_position}"  # Node identifier now reflects its physical location
            if col + 1 < len(shape):  # If not the last column
                transitions = {}
                next_x_position = start_x + col + 1
                next_y_start = start_y  # Starting y position for the next column
                for next_pos in range(shape[col + 1]):
                    next_y_position = start_y - next_pos
                    next_node = f"{next_x_position}_{next_y_position}"
                    # Calculate cost based on y-position difference
                    cost = calculate_cost(x_position, y_position, next_x_position, next_y_position, current_velocity)
                    transitions[next_node] = cost
                    next_y_start -= 1  # Move down for the next node in the column
                graph[node] = transitions
            else:
                transitions = {}
                cost = calculate_cost(x_position, y_position, end_x, end_y, 0)
                transitions[f"{end_x}_{end_y}"] = cost
                graph[node] = transitions
            y_position -= 1  # Move down for the next node in the same column
    return graph

shape = calculate_shape(start_x, start_y, end_x, end_y, starting_velocity)
graph = generate_graph_physical(shape, start_x, start_y, end_x, end_y, starting_velocity)
# print(graph)

final_state = f"{end_x}_{end_y}"
costs = {state: (float('inf'), None) for state in graph}
costs[final_state] = (0, None)

for state in reversed(list(graph.keys())[:-1]):
    for next_state, transition_cost in graph[state].items():
        total_cost = transition_cost + costs[next_state][0]
        if total_cost < costs[state][0]:
            costs[state] = (total_cost, next_state)

optimal_path = [f"{start_x}_{start_y}"]
current_state = f"{start_x}_{start_y}"

while current_state != final_state:
    next_state = costs[current_state][1]
    if next_state is None:
        optimal_path.append(final_state)
        break
    optimal_path.append(next_state)
    current_state = next_state

print(optimal_path)

