import random
import matplotlib.pyplot as plt

random.seed(42)

start_x=0
start_y=50
end_x=25
end_y=20
starting_velocity = 0

g = 9.81

def calculate_shape(start_x, start_y, end_x, end_y, starting_velocity):
    x_range = abs(end_x - start_x + 1)
    y_range = round((start_y - end_y)*3)
    shape = [y_range] * x_range
    return shape

def calculate_current_velocity(start_y, by, starting_velocity):
    h_diff = start_y - by
    effective_h_diff = h_diff if h_diff > 0 else 0
    vx = (2 * g * effective_h_diff+starting_velocity)**0.5
    return vx

def calculate_cost(ax, ay, bx, by, vx):
    vc = vx
    h_diff = ay - by
    effective_h_diff = h_diff if h_diff > 0 else 0
    vx = (2 * g * effective_h_diff + vx)**0.5
    s_ax = ((ax - bx)**2 + (ay - by)**2)**0.5
    v_ax = (vx + vc) / 2  
    time = s_ax / v_ax if v_ax != 0 else float('inf')
    return time

def generate_graph_physical(shape, start_x, start_y, end_x, end_y, current_velocity):
    graph = {}
    for col in range(len(shape)): # Outer loop for columns
        x_position = start_x + col
        y_position = start_y
        for pos in range(shape[col]): # Inner Loop for rows within each column
            y_position = start_y - pos
            node = f"{x_position}_{y_position}"
            current_velocity = calculate_current_velocity(start_y, y_position, starting_velocity)
            if col + 1 < len(shape):  # If not the last column
                transitions = {}
                next_x_position = start_x + col + 1
                next_y_start = start_y
                for next_pos in range(shape[col + 1]): # Nested loop for possible transitions
                    next_y_position = start_y - next_pos
                    next_node = f"{next_x_position}_{next_y_position}"
                    cost = calculate_cost(x_position, y_position, next_x_position, next_y_position, current_velocity)
                    transitions[next_node] = cost
                    next_y_start -= 1  # Move down for the next node in the column
                graph[node] = transitions
            else:
                current_velocity = calculate_current_velocity(start_y, y_position, starting_velocity)
                cost = calculate_cost(x_position, y_position, end_x, end_y, current_velocity)
                transitions[f"{end_x}_{end_y}"] = cost
                graph[node] = transitions
            y_position -= 1  # Move down for the next node in the same column
    return graph

shape = calculate_shape(start_x, start_y, end_x, end_y, starting_velocity)
graph = generate_graph_physical(shape, start_x, start_y, end_x, end_y, starting_velocity)

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

# Extracting x and y coordinates from the path
x_coords = [int(node.split('_')[0]) for node in optimal_path]
y_coords = [int(node.split('_')[1]) for node in optimal_path]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label='Optimized Path')
plt.scatter(x_coords, y_coords, color='red')  # Mark each point for clarity

# Setting labels and title
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Optimized Path from Start to End')
plt.legend()
plt.grid(True)
plt.show()
