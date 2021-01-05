import random

import matplotlib.pyplot as plt
import numpy as np


def generate_situation(number_tasks, task_stations):
    # Nodes to visit
    index_list = np.arange(0, len(task_stations))
    random.shuffle(index_list)
    task_locations = [task_stations[index_list[i]] for i in range(number_tasks)]
    return task_locations


def plot_situation(robot_locations, task_locations, graph):
    plt.figure()

    # Plot layout
    for node in graph:
        plt.plot(node.pos[0], node.pos[1], 'b.', ms=6)
        plt.text(node.pos[0], node.pos[1] + 0.1, node.name)
        for neighbor in node.neighbors:
            plt.plot([node.pos[0], neighbor.pos[0]], [node.pos[1], neighbor.pos[1]], 'b-', lw=0.5)

    # Plot tasks
    [plt.plot(x, y, 'gs', ms=7) for (x, y) in task_locations]

    # Plot robots
    [plt.plot(x, y, 'o', ms=10) for (x, y) in robot_locations]

    plt.title('Situation')
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.show()


def save_situation(task_locations, orders_file):
    file1 = open(orders_file, "w")
    for i in range(len(task_locations)):
        file1.write(str(task_locations[i][0]) + ",")
        file1.write(str(task_locations[i][1]) + ",\n")
    file1.close()


def read_situation(orders_file):
    location_tasks = []
    file1 = open(orders_file, "r")
    line = file1.readline()
    position = line.split(',')
    while line != "":
        pos = tuple((int(position[0]), int(position[1])))
        location_tasks.append(pos)
        line = file1.readline()
        position = line.split(',')
    file1.close()
    return location_tasks
