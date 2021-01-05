import numpy as np

from src.tasks.MotionPlanning import MotionPlanning
from src.utils.evaluator import *

from src.Graph import Graph

import matplotlib.pyplot as plt


class SSISolver:

    def __init__(self, speed, graph):

        # Params
        self.speed = speed
        self.graph = graph

        # Routing solver
        self.mp_solver = MotionPlanning(graph, speed)

    def solve(self, robots, task_locations, epsilon):

        # Params
        nrob = len(robots)
        ntask = len(task_locations)

        # Get solution
        if nrob == 1:
            solution = list(np.ones((nrob, ntask)))
            optimized_routes = convert_solution_to_routes(solution, robots, task_locations, graph)
            travel_time = calculate_travel_cost(optimized_routes[0], self.graph, self.speed)
            all_wanted_slots = {}
            total_delay = {'default': 0}
            total_path_cost = {'default': travel_time}
            total_execution_time = {'default': travel_time}
            congestions = 0
        else:

            # Initialize task lists
            local_task_lists = [[] for _ in robots]

            # Task list
            task_list = task_locations.copy()

            # Initialize solution matrix
            solution = np.zeros((len(robots), len(task_list)))
            all_wanted_slots = {}
            total_delay = {}
            total_path_cost = {}
            total_execution_time = {}

            # Auction, bid task by task
            for i in range(len(task_locations)):

                # Init bids
                bids = np.zeros((len(robots), len(task_list)))

                # Init routing info
                routes = {}
                slots = {}
                delays = {}

                # Bidding
                for j in range(len(robots)):
                    for k in range(len(task_list)):
                        new_objective, new_route, new_slots, new_delay = self.compute_bid(robots[j],
                                                                                          local_task_lists[j],
                                                                                          task_list[k], epsilon)
                        bids[j][k] = new_objective
                        routes[j, k] = new_route
                        slots[j, k] = new_slots
                        delays[j, k] = new_delay

                # Resolution
                winning_robot, winning_task = self.resolution_lb(bids)
                solution[winning_robot, task_locations.index(task_list[winning_task])] = 1

                # Update local task lists with optimal insertion
                new_local_task_list = local_task_lists[winning_robot] + [task_list[winning_task]]
                optimal_sequence, _, _ = optimal_insertion_solve(self.graph, robots[winning_robot]['Location'],
                                                                 new_local_task_list)
                local_task_lists[winning_robot] = optimal_sequence

                # Remove reservations of winning robot
                self.graph.remove_reservations(robots[winning_robot]['ID'])

                if not len(routes[winning_robot, winning_task]) == 1:

                    # Make new reservations for new tour
                    self.mp_solver.intent(robots[winning_robot]['ID'], routes[winning_robot, winning_task],
                                          slots[winning_robot, winning_task])

                    # Save new slots and delay for winning robot
                    all_wanted_slots[str(robots[winning_robot]['ID'])] = slots[winning_robot, winning_task]
                    total_delay[str(robots[winning_robot]['ID'])] = delays[winning_robot, winning_task]

                    # Compute path cost and execution time
                    path_cost = calculate_travel_cost(routes[winning_robot, winning_task], self.graph, self.speed)
                    total_path_cost[str(robots[winning_robot]['ID'])] = path_cost
                    total_execution_time[str(robots[winning_robot]['ID'])] = path_cost + delays[winning_robot, winning_task]

                # Remove task from task list
                del task_list[winning_task]

            congestions = check_congestions(all_wanted_slots)

        return {'solution': solution, 'all_wanted_slots': all_wanted_slots, 'congestions': congestions,
                'total_delay': sum([total_delay[key] for key in total_delay.keys()]),
                'total_path_cost': sum([total_path_cost[key] for key in total_delay.keys()]),
                'total_execution_time': max(total_execution_time.values()),
                "objective": (epsilon * sum([total_path_cost[key] for key in total_delay.keys()])
                              + (1 - epsilon) * max(total_execution_time.values()))}

    def compute_bid(self, robot, local_task_list, task, epsilon):

        # Compute current route
        current_route, current_slots, current_delay = self.mp_solver.dmas(robot['ID'], robot['Location'],
                                                                          local_task_list)

        # Evaluate current route
        current_cost = calculate_travel_cost(current_route, self.graph, self.speed) + current_delay

        # Compute new route
        new_route, new_slots, new_delay = self.mp_solver.dmas(robot['ID'], robot['Location'], local_task_list + [task])

        # Evaluate new route
        new_cost = calculate_travel_cost(new_route, self.graph, self.speed) + new_delay

        # Compute objective
        min_sum = new_cost - current_cost
        min_max = new_cost
        objective = (epsilon * min_sum + (1 - epsilon) * min_max)
        return objective, new_route, new_slots, new_delay

    @staticmethod
    def resolution_lb(bids):
        return np.unravel_index(bids.argmin(), bids.shape)


if __name__ == "__main__":

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

    # Other robot reserved slot
    graph.nodes['pos_12'].environmental_agent.reserve_slot((60, 20), "2")

    # Robot
    robot = {'ID': 1, 'Location': "pos_2", 'InitialResources': 100}

    # Local task list
    local_task_list = []

    # Task
    task = "pos_13"

    # Epsilon
    epsilon = 0

    # Solver
    ssi_solver = SSISolver(1, graph)

    # Compute bid
    objective, new_route, new_slots, new_delay = ssi_solver.compute_bid(robot, local_task_list, task, epsilon)

    print()
    print("Objective: " + str(objective))
    print("Route: " + str(new_route))
    print("Slots: " + str(new_slots))
    print("Delay: " + str(new_delay))

