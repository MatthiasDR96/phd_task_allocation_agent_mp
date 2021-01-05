import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()


def make_filename(robots_array, tasks_array, experiments_array, approaches, epsilon):
    # Make file name
    robot_text = str(robots_array[0]) + "-" + str(robots_array[-1]) + "R_"
    task_text = str(tasks_array[0]) + "-" + str(tasks_array[-1]) + "T_"
    experiment_text = str(experiments_array[0]) + "-" + str(experiments_array[-1]) + "E"
    solver_text = ""
    for solver in approaches:
        solver_text += "_" + solver
    epsilon_text = "_" + str(epsilon)
    filename = '../Data/experiment_' + robot_text + task_text + experiment_text + solver_text + epsilon_text + '.xlsx'
    return filename


def make_figures(robots_array, tasks_array, experiments_array, approaches, epsilon):

    # Make pandas dataframe
    cols = ['robots', 'tasks', 'objective', 'criterium', 'value']
    filename = make_filename(robots_array, tasks_array, experiments_array, approaches, epsilon)
    df = pd.read_excel(filename, columns=cols)

    # Loop through robots
    for num_robots in robots_array:

        # Save plots
        criteria = ['min_sum', 'min_max', 'objective', 'time_value', 'congestions', 'delay']
        if num_robots == 1:
            titles = ['Total cost for ' + str(num_robots) + ' robot', 'Time span for ' + str(num_robots) + ' robot',
                      'Objective for ' + str(num_robots) + ' robot',
                      'Computation time for ' + str(num_robots) + ' robot',
                      'Amount of congestions for ' + str(num_robots) + ' robot',
                      'Total delay for ' + str(num_robots) + ' robot']
        else:
            titles = ['Total cost for ' + str(num_robots) + ' robots',
                      'Time span for ' + str(num_robots) + ' robots',
                      'Objective for ' + str(num_robots) + ' robots',
                      'Computation time for ' + str(num_robots) + ' robots',
                      'Amount of congestions for ' + str(num_robots) + ' robot',
                      'Total delay for ' + str(num_robots) + ' robot']
        ylabels = ['Total cost of the assignment (s)', 'Time span of the assignment (s)', 'Objective value',
                   'Time (s)', 'Amount of congestions', 'Total delay (s)']
        plot_files = ['total_path_cost', 'total_time_span', 'objective', 'computation_time',
                      'congestions', 'total_delay']

        for i in range(len(criteria)):
            criterium = criteria[i]
            fig, ax = plt.subplots()
            df1 = df[(df['robots'] == num_robots) & (df['objective'] == 'OPT') & (df['criterium'] == criterium)]
            df2 = df[(df['robots'] == num_robots) & (df['objective'] == 'SSI') & (df['criterium'] == criterium)]
            df3 = df[(df['robots'] == num_robots) & (df['objective'] == 'HEUR') & (df['criterium'] == criterium)]
            sns.lineplot(x='tasks', y='value', data=df1, ax=ax, marker='.', color="b", label="Optimal")
            sns.lineplot(x='tasks', y='value', data=df2, ax=ax, marker='^', color="orange", label="SSI")
            sns.lineplot(x='tasks', y='value', data=df3, ax=ax, marker='*', color="g", label="Heuristic")
            ax.legend()
            plt.title(titles[i])
            plt.xlabel("Amount of tasks")
            plt.ylabel(ylabels[i])
            plt.savefig('../Pictures/' + plot_files[i] + '_' + str(num_robots) + '_robots' + '.png', dpi=400)
            plt.clf()


def calculate_simulation_time(num_tasks, num_robots):
    f = 340 / (3 ** 10)
    total_time = 0
    for i in range(1, num_tasks + 1):
        for j in range(1, num_robots + 1):
            number_of_possibilities = j ** i
            time_ = number_of_possibilities * f
            total_time += time_
    print("\nTotal simulation will take about: " + str(total_time / 60) + " minutes")


def plot_layout(graph):
    plt.figure("Layout")
    for node in graph.nodes:
        plt.plot(node.pos[0], node.pos[1], 'k.', ms=5)
        for neighbor in node.neighbors:
            plt.plot([node.pos[0], neighbor.pos[0]], [node.pos[1], neighbor.pos[1]], 'k-', lw=0.5)
    plt.axis('square')
    plt.title("Layout")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.ylabel('y-coordinate')
    plt.xlabel('x-coordinate')
    plt.savefig('../Pictures/layout.png', dpi=400)
    plt.clf()


def plot_assignment(graph, assignment, tours, robots, num_tasks, type_):
    # Make figure
    plt.figure('Assignment')
    plt.axis('square')
    plt.title("Assignment")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.ylabel('y-coordinate')
    plt.xlabel('x-coordinate')
    colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(robots)))

    # Plot layout
    for node_name in graph.nodes.keys():
        node = graph.nodes[node_name]
        plt.plot(node.pos[0], node.pos[1], 'k.', ms=5)
        for neighbor_name in node.neighbors:
            neighbor = graph.nodes[neighbor_name]
            plt.plot([node.pos[0], neighbor.pos[0]], [node.pos[1], neighbor.pos[1]], 'k-', lw=0.5)

    # Plot robots
    [plt.plot(robots[i]['Location'][0], robots[i]['Location'][1], 'o', ms=10, color=colors[i])
     for i in range(len(robots))]

    # Plot assignment
    for i in range(len(assignment)):
        for item in assignment[i]:
            plt.plot(item[0], item[1], 'gs', ms=7)
            plt.plot([robots[i]['Location'][0], item[0]],
                     [robots[i]['Location'][1], item[1]], color=colors[i], lw=0.5)

    # Plot paths
    for i in range(len(assignment)):
        if assignment[i]:
            path = tours[i]
            for k in range(len(path) - 1):
                plt.plot([path[k].pos[0], path[k + 1].pos[0]], [path[k].pos[1], path[k + 1].pos[1]], color=colors[i],
                         lw=3)
            for j in range(len(assignment[i]) - 1):
                path = feasibility_solver.solve(graph, robots[i]['Location'], assignment[i][0])
                for k in range(len(path) - 1):
                    plt.plot([path[k].pos[0], path[k + 1].pos[0]], [path[k].pos[1], path[k + 1].pos[1]],
                             color=colors[i], lw=3)
    plt.savefig('../Pictures/assignment_' + str(num_tasks) + type_ + '.png', dpi=400)
    plt.clf()


def plot_solution(solution, robot_locations, task_locations):
    [plt.plot(x, y, 'b.') for (x, y) in task_locations]
    [plt.plot(x, y, 'r.') for (x, y) in robot_locations]
    for i in range(len(solution)):
        local_task_list = solution[i]
        if local_task_list:
            plt.plot((robot_locations[i][0], local_task_list[0][0]),
                     (robot_locations[i][1], local_task_list[0][1]), 'r-')
            for j in range(len(local_task_list) - 1):
                plt.plot([local_task_list[j][0], local_task_list[j + 1][0]],
                         [local_task_list[j][1], local_task_list[j + 1][1]], 'r-')
    plt.title('Solution')
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.show()
