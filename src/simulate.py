import time
from multiprocessing import Pool
from src.solvers.HeuristicSolver import HeuristicSolver
from src.solvers.OptimalSolver import OptimalSolver
from src.solvers.SSISolver import SSISolver
from src.utils.evaluator import *
from src.utils.situation_generator import *
from src.utils.utils import *
from src.RoutingEvaluator import RoutingEvaluator


def simulate(ntasks, nrobots, nexperiments, approaches, params):

    # Start clock
    main_tic = time.perf_counter()

    # Create experiment arrays
    tasks_array = np.arange(5, ntasks + 1)
    robots_array = np.arange(3, nrobots + 1)
    experiments_array = np.arange(1, nexperiments + 1)

    # Init solvers
    opt_sol = None
    heur_sol = None
    ssi_sol = None

    # Create evaluator
    r_eval = RoutingEvaluator(params['speed'], params['graph'])

    # Create optimal solver
    if 'OPT' in approaches:
        opt_sol = OptimalSolver(params['speed'], params['graph'])

    # Create heuristic solver
    if 'HEUR' in approaches:
        heur_sol = HeuristicSolver(params['speed'], params['graph'])

    # Create SSI solver
    if 'SSI' in approaches:
        ssi_sol = SSISolver(params['speed'], params['graph'])

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
                task_locations = generate_situation(num_tasks, params['task_names'])

                # Get robots
                robots = []
                for i in range(num_robots):
                    robots.append({'ID': i, 'Location': params['depot_names'][i % 3], 'InitialResources': 100})

                with Pool(processes=len(approaches)) as pool:

                    # Get optimal solution
                    if 'OPT' in approaches:
                        print("\t\t\tOPT")

                        # Solve
                        tic = time.perf_counter()
                        opt_solution = pool.starmap(opt_sol.solve, [(robots, task_locations, params['epsilon'])])[0]
                        toc = time.perf_counter()
                        time_value_opt = toc - tic

                        # Evaluate
                        opt_evaluation = evaluate_solution(opt_solution, robots, task_locations, params['speed'], params['graph'], params['epsilon'])

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
                        heur_solution = pool.starmap(heur_sol.solve, [(robots, task_locations, params['epsilon'])])[0]
                        toc = time.perf_counter()
                        time_value_heur = toc - tic

                        # Evaluation
                        heur_evaluation = r_eval.evaluate_solution(heur_solution, robots, task_locations, params['graph'], params['speed'],
                                                                   params['epsilon'])

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
                        ssi_solution = pool.starmap(ssi_sol.solve, [(robots, task_locations, params['epsilon'])])[0]
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
        filename = make_filename(robots_array, tasks_array, experiments_array, approaches, params['epsilon'])
        df.to_excel(filename)

    # To excel files
    cols = ['robots', 'tasks', 'objective', 'criterium', 'value']
    df = pd.DataFrame(lst, columns=cols)
    filename = make_filename(robots_array, tasks_array, experiments_array, approaches, params['epsilon'])
    df.to_excel(filename)

    # Stop clock
    main_toc = time.perf_counter()
    sim_time = main_toc - main_tic
    print("\nTotal simulation time: " + str(sim_time / 60) + " minutes.")
