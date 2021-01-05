from src.tasks.MotionPlanning import MotionPlanning
from src.utils.evaluator import *
from src.Graph import Graph
from src.utils.situation_generator import *


class RoutingEvaluator:

    def __init__(self, speed, graph):

        # Params
        self.speed = speed
        self.graph = graph

        # Routing solver
        self.mp_solver = MotionPlanning(graph, speed)

    def evaluate_solution(self, solution, robots, task_locations, graph, speed, epsilon):

        # Create optimal path for each robot (list of node names)
        optimized_routes = convert_solution_to_routes(solution, robots, task_locations, graph)

        # Compute cost metrics for each robot
        all_wanted_slots = {node_name: [] for node_name in graph.nodes.keys()}
        total_path_cost = 0
        total_execution_time = 0
        delay = 0
        for i in range(len(optimized_routes)):

            # Get route of robot
            optimized_route = optimized_routes[i]

            # Check wanted slots
            travel_time = 0
            if len(optimized_route) > 1:
                all_wanted_slots, travel_time = self.check_wanted_slots(all_wanted_slots, optimized_route)

            # Compute execution time
            execution_time = travel_time

            # Compute cost metrics
            total_path_cost += travel_time
            if execution_time > total_execution_time:
                total_execution_time = execution_time

        # Check congestions
        total_congestions = check_congestions(all_wanted_slots)

        evaluation = {"solution": solution, "total_path_cost": total_path_cost, 'total_delay': delay,
                      "total_execution_time": total_execution_time, 'congestions': total_congestions,
                      "objective": (epsilon * total_path_cost + (1 - epsilon) * total_execution_time)}

        return evaluation

    def check_wanted_slots(self, all_wanted_slots, path):

        # Init
        timestamp = 0
        total_travel_time = 0

        # Calculate slot of first node
        travel_time = self.graph.edges[path[0], path[1]].length / self.speed / 2
        all_wanted_slots[path[0]].append((timestamp, travel_time))
        total_travel_time += travel_time
        timestamp += travel_time

        # Calculate slot of nodes in between
        for i in range(1, len(path) - 1):
            travel_time_1 = self.graph.edges[path[i - 1], path[i]].length / self.speed / 2
            travel_time_2 = self.graph.edges[path[i], path[i + 1]].length / self.speed / 2
            all_wanted_slots[path[i]].append((timestamp, travel_time_1 + travel_time_2))
            total_travel_time += travel_time_1 + travel_time_2
            timestamp += travel_time_1 + travel_time_2

        # Calculate slot of last node
        travel_time = self.graph.edges[path[-2], path[-1]].length / self.speed / 2
        all_wanted_slots[path[-1]].append((timestamp, travel_time))
        total_travel_time += travel_time
        timestamp += travel_time

        return all_wanted_slots, total_travel_time


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

    # Get random task list (list of node names)
    task_locations = generate_situation(9, task_names)

    # Get robots
    robots = []
    for i in range(2):
        robots.append({'ID': i, 'Location': depot_names[i % 3], 'InitialResources': 100})

    # Evaluator
    mp_eval = RoutingEvaluator(speed, graph)

    # Solution
    solution = np.array([[1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1]])

    # Check wanted slots
    evaluation = mp_eval.evaluate_solution(solution, robots, task_locations, graph, speed, epsilon)
    print("Total path cost: " + str(evaluation['total_path_cost']))
    print("Total execution time: " + str(evaluation['total_execution_time']))
    print("Amount of congestions: " + str(evaluation['congestions']))
