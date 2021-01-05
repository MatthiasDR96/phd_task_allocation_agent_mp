import time
from multiprocessing import Pool
from src.Graph import Graph
from src.solvers.HeuristicSolver import HeuristicSolver
from src.solvers.OptimalSolver import OptimalSolver
from src.solvers.SSISolver import SSISolver
from src.utils.evaluator import *
from src.utils.situation_generator import *
from src.utils.utils import *
from src.RoutingEvaluator import RoutingEvaluator

if __name__ == "__main__":

    # Start clock
    main_tic = time.perf_counter()

    # Create situation #

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

    # Create experiment arrays
    tasks_array = np.arange(5, ntasks + 1)
    robots_array = np.arange(3, nrobots + 1)
    experiments_array = np.arange(1, nexperiments + 1)

    # Init solvers
    opt_sol = None
    heur_sol = None
    ssi_sol = None

    # Create evaluator
    r_eval = RoutingEvaluator(speed, graph)

    # Create optimal solver
    if 'OPT' in approaches:
        opt_sol = OptimalSolver(speed, graph)

    # Create heuristic solver
    if 'HEUR' in approaches:
        heur_sol = HeuristicSolver(speed, graph)

    # Create SSI solver
    if 'SSI' in approaches:
        ssi_sol = SSISolver(speed, graph)

    # Data structure to save all data
    lst = []

    # Start simulation
    for num_robots in robots_array:

        # Simulation status
        print("\nAmount of robots: " + str(num_robots))

        for num_tasks in tasks_array:

            # Simulation status
            print("\tAmount of tasks: " + str(num_tasks))

            for num_experiments in experiments_array:

                # Simulation status
                print("\t\tExperiment: " + str(num_experiments))

                # Get random task list (list of node names)
                task_locations = generate_situation(num_tasks, task_names)

                # Get robots
                robots = []
                for i in range(num_robots):
                    robots.append({'ID': i, 'Location': depot_names[i % 3], 'InitialResources': 100})

                with Pool(processes=len(approaches)) as pool:

                    # Get optimal solution
                    if 'OPT' in approaches:

                        print("\t\t\tOPT")

                        # Solve
                        tic = time.perf_counter()
                        opt_solution = pool.starmap(opt_sol.solve, [(robots, task_locations, epsilon)])[0]
                        toc = time.perf_counter()
                        time_value_opt = toc - tic

                        # Evaluate
                        opt_evaluation = evaluate_solution(opt_solution, robots, task_locations, graph, speed, epsilon)

                        # Save results
                        lst.append([num_robots, num_tasks, 'OPT', 'time_value', time_value_opt])
                        lst.append([num_robots, num_tasks, 'OPT', 'min_sum', opt_evaluation["total_path_cost"]])
                        lst.append([num_robots, num_tasks, 'OPT', 'min_max', opt_evaluation["total_execution_time"]])
                        lst.append([num_robots, num_tasks, 'OPT', 'objective', opt_evaluation["objective"]])

                    # Get heuristic solution
                    if 'HEUR' in approaches:

                        print("\t\t\tHEUR")

                        # Solve
                        tic = time.perf_counter()
                        heur_solution = pool.starmap(heur_sol.solve, [(robots, task_locations, epsilon)])[0]
                        toc = time.perf_counter()
                        time_value_heur = toc - tic

                        # Evaluation
                        heur_evaluation = r_eval.evaluate_solution(heur_solution, robots, task_locations, graph, speed,
                                                                   epsilon)

                        # Save results
                        lst.append([num_robots, num_tasks, 'HEUR', 'time_value', time_value_heur])
                        lst.append([num_robots, num_tasks, 'HEUR', 'min_sum', heur_evaluation["total_path_cost"]])
                        lst.append([num_robots, num_tasks, 'HEUR', 'min_max', heur_evaluation["total_execution_time"]])
                        lst.append([num_robots, num_tasks, 'HEUR', 'objective', heur_evaluation["objective"]])
                        lst.append([num_robots, num_tasks, 'HEUR', 'delay', heur_evaluation['total_delay']])
                        lst.append([num_robots, num_tasks, 'HEUR', 'congestions', heur_evaluation["congestions"]])

                    # Get SSI solution
                    if 'SSI' in approaches:

                        print("\t\t\tSSI")

                        # Solve
                        tic = time.perf_counter()
                        ssi_solution = pool.starmap(ssi_sol.solve, [(robots, task_locations, epsilon)])[0]
                        toc = time.perf_counter()
                        time_value_ssi = toc - tic

                        # Save results
                        lst.append([num_robots, num_tasks, 'SSI', 'time_value', time_value_ssi])
                        lst.append([num_robots, num_tasks, 'SSI', 'min_sum', ssi_solution["total_path_cost"]])
                        lst.append([num_robots, num_tasks, 'SSI', 'min_max', ssi_solution["total_execution_time"]])
                        lst.append([num_robots, num_tasks, 'SSI', 'objective', ssi_solution["objective"]])
                        lst.append([num_robots, num_tasks, 'SSI', 'delay', ssi_solution['total_delay']])
                        lst.append([num_robots, num_tasks, 'SSI', 'congestions', ssi_solution["congestions"]])

        # To excel files
        cols = ['robots', 'tasks', 'objective', 'criterium', 'value']
        df = pd.DataFrame(lst, columns=cols)
        filename = make_filename(robots_array, tasks_array, experiments_array, approaches, epsilon)
        df.to_excel(filename)

    # To excel files
    cols = ['robots', 'tasks', 'objective', 'criterium', 'value']
    df = pd.DataFrame(lst, columns=cols)
    filename = make_filename(robots_array, tasks_array, experiments_array, approaches, epsilon)
    df.to_excel(filename)

    # Stop clock
    main_toc = time.perf_counter()
    sim_time = main_toc - main_tic
    print("\nTotal simulation time: " + str(sim_time / 60) + " minutes.")
