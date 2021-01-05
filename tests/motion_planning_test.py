import math
import random

import matplotlib.pyplot as plt
import numpy as np

from src.Graph import Graph
from src.tasks.MotionPlanning import MotionPlanning

if __name__ == "__main__":

    # Create graph
    node_locations = [(10, 30), (10, 50), (10, 70), (30, 10), (30, 30), (30, 50), (30, 70), (30, 90), (60, 10),
                      (60, 30), (60, 50), (60, 70), (60, 90), (90, 10), (90, 50), (90, 90)]
    node_names = ["pos_1", "pos_2", "pos_3", "pos_4", "pos_5", "pos_6", "pos_7", "pos_8", "pos_9", "pos_10",
                  "pos_11", "pos_12", "pos_13", "pos_14", "pos_15", "pos_16"]
    depot_names = ["pos_1", "pos_2", "pos_3"]
    other_names = ["pos_4", "pos_5", "pos_6", "pos_7", "pos_8", "pos_9", "pos_10", "pos_11", "pos_12", "pos_13",
                   "pos_14", "pos_15", "pos_16"]
    node_neighbors = [["pos_5"], ["pos_6"], ["pos_7"], ["pos_5", "pos_9"], ["pos_1", "pos_4", "pos_6"],
                      ["pos_2", "pos_5", "pos_7", "pos_10", "pos_11", "pos_12"],
                      ["pos_3", "pos_6", "pos_8"], ["pos_7", "pos_13"], ["pos_4", "pos_10", "pos_14"],
                      ["pos_6", "pos_9", "pos_11"],
                      ["pos_6", "pos_10", "pos_12", "pos_15"], ["pos_6", "pos_11", "pos_13"],
                      ["pos_8", "pos_12", "pos_16"], ["pos_15", "pos_9"], ["pos_11", "pos_14", "pos_16"],
                      ["pos_13", "pos_15"]]
    node_neighbors_uni = [["pos_5"], ["pos_6"], ["pos_7"], ["pos_9"], ["pos_4"],
                          ["pos_5", "pos_10", "pos_11", "pos_12"],
                          ["pos_6"], ["pos_7"], ["pos_10", "pos_14"],
                          ["pos_6", "pos_9", "pos_11"],
                          ["pos_6", "pos_10", "pos_12", "pos_15"], ["pos_6", "pos_11", "pos_13"],
                          ["pos_8", "pos_12", "pos_16"], ["pos_15", "pos_9"], ["pos_11", "pos_14", "pos_16"],
                          ["pos_13", "pos_15"]]

    # Create graph
    graph = Graph()
    graph.create_nodes(node_locations, node_names)
    graph.create_edges(node_names, node_neighbors_uni)

    # Test vectors
    amount_of_locations = 2
    amount_of_robots = 3

    # Start nodes
    start_nodes = []
    for i in range(amount_of_robots):
        start_nodes.append(depot_names[i % 3])

    # Nodes to visit
    index_list = np.arange(0, len(other_names))
    random.shuffle(index_list)
    nodes_to_visit = []
    for i in range(amount_of_robots):
        nodes_to_visit.append([other_names[index_list[i]] for i in range(amount_of_locations)])
        random.shuffle(index_list)

    # Agents
    agents = []
    for i in range(amount_of_robots):
        agents.append(MotionPlanning(graph, 1))

    # Do dmas
    paths = []
    for i in range(amount_of_robots):
        best_path, best_slots, best_delay = agents[i].dmas(str(i), start_nodes[i], nodes_to_visit[i])
        agents[i].intent(str(i), best_path, best_slots)
        paths.append(best_path)

    # Count not empty node schedules
    count_n = 0
    for node in graph.nodes.values():
        if not len(node.environmental_agent.reservations) == 0:
            count_n += 1

    # Plot node schedules
    fig, axes = plt.subplots(nrows=round(math.sqrt(count_n)) + 1, ncols=round(count_n / round(math.sqrt(count_n))),
                             gridspec_kw={'hspace': 1.5, 'wspace': 0.5})
    axes = axes.ravel()
    nodes = list(graph.nodes.values())
    i = 0
    for node in graph.nodes.values():
        if not len(node.environmental_agent.reservations) == 0:
            node.environmental_agent.plot(axes[i])
            i += 1

    # Plot paths
    fig, axes = plt.subplots(nrows=1, ncols=amount_of_robots, gridspec_kw={'hspace': 1.5, 'wspace': 0.5})
    axes = axes.ravel()
    colors = ['r', 'g', 'b']
    for i in range(amount_of_robots):
        path = paths[i]
        ax = axes[i]

        # Plot layout
        graph.plot(ax)
        for node in graph.nodes.values():
            ax.plot(node.pos[0], node.pos[1], 'k.', ms=6)
            for neighbor in node.neighbors:
                neighbor_node = graph.nodes[neighbor]
                ax.plot([node.pos[0], neighbor_node.pos[0]], [node.pos[1], neighbor_node.pos[1]], 'k-', lw=0.5)

        # Plot paths
        if path:
            path_ = [graph.nodes[name] for name in path]
            for k in range(len(path) - 1):
                ax.plot([path_[k].pos[0], path_[k + 1].pos[0]], [path_[k].pos[1], path_[k + 1].pos[1]],
                        color=colors[i % 3],
                        marker='.', ms=10)

        # Plot nodes to visit
        for node_name in nodes_to_visit[i]:
            node = graph.nodes[node_name]
            ax.plot(node.pos[0], node.pos[1], 'k.', ms=15)
    plt.show()
