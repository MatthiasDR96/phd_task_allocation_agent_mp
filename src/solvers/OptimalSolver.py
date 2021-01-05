import numpy as np

from src.utils.evaluator import *


class OptimalSolver:

    def __init__(self, speed, graph):

        # Params
        self.speed = speed
        self.graph = graph

    def solve(self, robots, task_locations, epsilon):

        # Params
        nrob = len(robots)
        ntask = len(task_locations)

        # Get solution
        if nrob == 1:
            solution = list(np.ones((nrob, ntask)))
        else:

            # Get all possible solutions
            all_possible_solutions = self.get_all_solution_combinations(robots, task_locations)

            # Brute force search
            solution = None
            best_objective = float('inf')
            cnt = 1
            for sol in all_possible_solutions:

                # Compute cost
                total_path_cost, total_execution_time = compute_solution_cost(sol, robots, task_locations,
                                                                              self.graph, self.speed)

                # Calculate objective
                objective = (epsilon * total_path_cost + (1 - epsilon) * total_execution_time)

                # Minimize
                if objective < best_objective:
                    best_objective = objective
                    solution = sol

                cnt += 1

        return solution

    @staticmethod
    def get_all_solution_combinations(robots, task_locations):
        solutions = []
        permutations = itertools.product(robots, repeat=len(task_locations))
        for each_permutation in permutations:
            solution = np.zeros((len(robots), len(task_locations)))
            for i in range(len(each_permutation)):
                solution[robots.index(each_permutation[i])][i] = 1
            solutions.append(solution)
        return solutions
