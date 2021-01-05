from src.utils.utils import *

# Experiment params
ntasks = 10
nrobots = 6
nexperiments = 5

# Create experiment arrays
tasks_array = np.arange(5, ntasks + 1)
robots_array = np.arange(3, nrobots + 1)
experiments_array = np.arange(1, nexperiments + 1)

approaches = ['HEUR', 'SSI']
epsilon = 0

make_figures(robots_array, tasks_array, experiments_array, approaches, epsilon)
