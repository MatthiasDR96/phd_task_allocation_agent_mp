from src.utils.optimal_insertion_solver import *


def evaluate_solution(solution, robots, task_locations, graph, speed, epsilon):
    total_path_cost, total_execution_time = compute_solution_cost(solution, robots, task_locations, graph, speed)

    evaluation = {"solution": solution, "total_path_cost": total_path_cost,
                  "total_execution_time": total_execution_time,
                  "objective": (epsilon * total_path_cost + (1 - epsilon) * total_execution_time)}

    return evaluation


def compute_solution_cost(solution, robots, task_locations, graph, speed):

    # Create optimal path for each robot (list of node names)
    optimized_routes = convert_solution_to_routes(solution, robots, task_locations, graph)

    # Compute cost metrics for each robot
    total_path_cost = 0
    total_execution_time = 0
    for i in range(len(optimized_routes)):

        # Get route of robot
        optimized_route = optimized_routes[i]

        # Compute travel cost
        path_cost = calculate_travel_cost(optimized_route, graph, speed)

        # Compute execution time
        execution_time = path_cost

        # Compute cost metrics
        total_path_cost += path_cost
        if execution_time > total_execution_time:
            total_execution_time = execution_time

    return total_path_cost, total_execution_time


def convert_solution_to_routes(solution, robots, task_locations, graph):
    optimized_routes = []
    num_robots = len(robots)
    num_tasks = len(task_locations)
    for i in range(num_robots):
        # Get robot
        robot = robots[i]

        # Get locations to visit
        nodes_to_visit = [task_locations[j] for j in range(num_tasks) if solution[i][j] == 1]

        # Get optimized_tour
        optimized_sequence, optimized_route, optimized_cost = optimal_insertion_solve(graph,
                                                                                      robot['Location'],
                                                                                      nodes_to_visit)
        optimized_routes.append(optimized_route)

    return optimized_routes


def calculate_travel_cost(route, graph, speed):
    path_cost = 0
    for i in range(len(route) - 1):
        distance = graph.edges[route[i], route[i + 1]].length
        travel_time = distance / speed
        path_cost += travel_time
    return path_cost


def check_congestions(all_wanted_slots):
    congestions = 0
    for key in all_wanted_slots.keys():
        node_reservations = all_wanted_slots[key]
        if len(node_reservations) > 1:
            for i in range(len(node_reservations)-1):
                for j in range(i+1, len(node_reservations)):
                    x = node_reservations[i]
                    y = node_reservations[j]
                    if y[0] <= x[0] < y[0] + y[1] or y[0] < x[0] \
                            + x[1] <= y[0] + y[1]:
                        # print("Congestion at node " + str(key) + ": " + str(x) + ', ' + str(y))
                        congestions += 1
    return congestions
