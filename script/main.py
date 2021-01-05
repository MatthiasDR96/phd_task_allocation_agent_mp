from src.Graph import Graph
from src.simulate import simulate


if __name__ == "__main__":

    # Set params
    speed = 1
    epsilon = 0

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

    # Create layout
    graph = Graph()
    graph.create_nodes(node_locations, node_names)
    graph.create_edges(node_names, node_neighbors)

    # Create simulation #

    # Experiment params
    ntasks = 10
    nrobots = 6
    nexperiments = 5
    approaches = ['HEUR', 'SSI']
    params = {"speed": speed, "epsilon": epsilon, "graph": graph, "task_names": task_names, "depot_names": depot_names}

    # Simulate
    simulate(ntasks, nrobots, nexperiments, approaches, params)