from src.utils.evaluator import *
from src.utils.genetic_algorithm_solver import *


class HeuristicSolver:

    def __init__(self, speed, graph):

        # Params
        self.speed = speed
        self.graph = graph

        # Fitness variables
        self.robots = None
        self.task_locations = None
        self.epsilon = None

    def solve(self, robots, task_locations, epsilon):

        # Save situation params
        self.robots = robots
        self.task_locations = task_locations
        self.epsilon = epsilon

        # Params
        nrob = len(self.robots)
        ntask = len(self.task_locations)

        # Get solution
        if nrob == 1:
            solution = list(np.ones((nrob, ntask)))
        else:

            # GA
            combinations = nrob ** ntask
            algorithm_param = {'max_num_iteration': min(1000, combinations * 10), 'population_size': 10 * nrob,
                               'mutation_probability': 0.1, 'elit_size': nrob, 'max_stall_generations': 10}

            # GA solver
            fitness = float('inf')
            solution = None
            cnt = 1
            while fitness == float('inf'):
                if cnt > 1:
                    print("Attempt " + str(cnt) + " of GA")
                solution, fitness = genetic_algorithm(self.fitness, (nrob, ntask), algorithm_param)
                cnt += 1

            # Convert optimal solution vector to optimal solution matrix
            solution = np.reshape(solution, (len(self.robots), len(self.task_locations)))

        return solution

    def fitness(self, x):

        # Convert solution vector to solution matrix
        solution = np.reshape(x, (len(self.robots), len(self.task_locations)))

        # Constraint, all tasks need to be executed
        pen = 0
        if not np.array_equal(list(solution.sum(axis=0)), list([1] * len(self.task_locations))):
            pen += float('inf')

        # Compute solution cost
        total_path_cost, total_execution_time = compute_solution_cost(solution, self.robots, self.task_locations,
                                                                      self.graph, self.speed)

        return (self.epsilon * total_path_cost + (1 - self.epsilon) * total_execution_time) + pen
