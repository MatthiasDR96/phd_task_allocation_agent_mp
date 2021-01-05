import numpy as np

from src.utils.feasibility_ant_solver import *


class MotionPlanning:
    """
                A class containing the intelligence of the Motion Planning agent
        """

    def __init__(self, graph, speed):

        # Params from parent agent (AGV)
        self.graph = graph
        self.speed = speed

    def dmas(self, agv_id, start_node, nodes_to_visit):

        if nodes_to_visit:

            # Feasibility ants
            global_feasible_path, local_feasible_paths = feasibility_ant_solve(self.graph, start_node, nodes_to_visit)

            # print("Local feasible paths: " + str(local_feasible_paths))

            if local_feasible_paths:

                # Exploration ants
                explored_paths, fitness_values, total_edge_costs, total_delays, slots = self.explore(agv_id,
                                                                                                     local_feasible_paths)

                # Best route selection
                best_path = explored_paths[int(np.argmin(fitness_values))]
                best_slots = slots[int(np.argmin(fitness_values))]
                best_delay = total_delays[int(np.argmin(fitness_values))]

                return best_path, best_slots, best_delay

            else:
                print("No feasible paths found")
                return None, None, None
        else:
            return [start_node], None, 0

    def explore(self, agv_id, paths):

        # Init
        fitness_values = []
        total_travel_costs = []
        total_delays = []
        all_slots = []

        # Explore paths
        for path in paths:

            # Init
            timestamp = 0
            total_delay = 0
            total_travel_time = 0
            slots = []

            # Calculate slot of first node
            travel_time = self.graph.edges[path[0], path[1]].length / self.speed / 2
            wanted_slot = (timestamp, travel_time)
            slot, delay = self.graph.nodes[path[0]].environmental_agent.check_slot(wanted_slot, agv_id)
            slots.append(slot)
            total_travel_time += travel_time
            total_delay += delay
            timestamp += travel_time + delay

            # Calculate slot of nodes in between
            for i in range(1, len(path) - 1):
                travel_time_1 = self.graph.edges[path[i - 1], path[i]].length / self.speed / 2
                travel_time_2 = self.graph.edges[path[i], path[i + 1]].length / self.speed / 2
                wanted_slot = (timestamp, travel_time_1 + travel_time_2)
                slot, delay = self.graph.nodes[path[i]].environmental_agent.check_slot(wanted_slot, agv_id)
                slots.append(slot)
                total_travel_time += travel_time_1 + travel_time_2
                total_delay += delay
                timestamp += travel_time_1 + travel_time_2 + delay

            # Calculate slot of last node
            travel_time = self.graph.edges[path[-2], path[-1]].length / self.speed / 2
            wanted_slot = (timestamp, travel_time)
            slot, delay = self.graph.nodes[path[-1]].environmental_agent.check_slot(wanted_slot, agv_id)
            slots.append(slot)
            total_travel_time += travel_time
            total_delay += delay
            timestamp += travel_time + delay

            # Collect results
            fitness_values.append(timestamp)
            total_travel_costs.append(total_travel_time)
            total_delays.append(total_delay)
            all_slots.append(slots)

        return paths, fitness_values, total_travel_costs, total_delays, all_slots

    def intent(self, agv_id, path, slots):

        for i in range(len(path)):
            # Destination node
            dest = path[i]

            # Wanted slot
            wanted_slot = slots[i]

            # Reserve slot
            self.graph.nodes[dest].environmental_agent.reserve_slot(wanted_slot, agv_id)
