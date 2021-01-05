from src.Graph import Graph
from src.utils.feasibility_ant_solver import *

# Define layout
node_locations = [(10, 30), (10, 50), (10, 70), (30, 10), (30, 30), (30, 50), (30, 70), (30, 90), (60, 10),
                  (60, 30), (60, 50), (60, 70), (60, 90), (90, 10), (90, 50), (90, 90)]
node_names = ["pos_1", "pos_2", "pos_3", "pos_4", "pos_5", "pos_6", "pos_7", "pos_8", "pos_9", "pos_10",
              "pos_11", "pos_12", "pos_13", "pos_14", "pos_15", "pos_16"]
depot_names = ["pos_1", "pos_2", "pos_3"]
task_names = ["pos_4", "pos_5", "pos_6", "pos_7", "pos_8", "pos_9", "pos_10", "pos_11", "pos_12", "pos_13",
              "pos_14", "pos_15", "pos_16"]
node_neighbors = [["pos_5"], ["pos_6"], ["pos_7"], ["pos_5", "pos_9"], ["pos_1", "pos_4", "pos_6"],
                  ["pos_2", "pos_5", "pos_7", "pos_10", "pos_11", "pos_12"],
                  ["pos_3", "pos_6", "pos_8"], ["pos_7", "pos_13"], ["pos_4", "pos_10", "pos_14"],
                  ["pos_6", "pos_9", "pos_11"],
                  ["pos_6", "pos_10", "pos_12", "pos_15"], ["pos_6", "pos_11", "pos_13"],
                  ["pos_8", "pos_12", "pos_16"], ["pos_15", "pos_9"], ["pos_11", "pos_14", "pos_16"],
                  ["pos_13", "pos_15"]]

# Create graph
graph = Graph()
graph.create_nodes(node_locations, node_names)
graph.create_edges(node_names, node_neighbors)

# Start node
start_node = 'pos_2'

# Nodes to visit
nodes_to_visit = ['pos_5', 'pos_9']

# Feasibility ants
global_feasible_path, local_feasible_paths = feasibility_ant_solve(graph, start_node, nodes_to_visit)

print("Global feasible path: " + str(global_feasible_path))
print("Local feasible paths: " + str(local_feasible_paths))
