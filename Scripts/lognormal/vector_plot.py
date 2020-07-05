#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import vector_results_aggregator
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter

# Checks the number of the input parameters, assigns the parameters to variables.
# 2 parameters = 2D plot (x,y)     3 parameters = 3D plot (x,y,z) (or multiple lines on 2D plot, (x-y,z))
if len(sys.argv) == 4:
	pass
else:
	print("USAGE: script_name path_dir_csv_with_final_slash <Y parameter name> <simulations_seconds>")
	sys.exit()

csv_directory = sys.argv[1]
parameter = sys.argv[2]
simulations_seconds = int(sys.argv[3])



x_values = np.arange(simulations_seconds)
# Aggregates csv files in the directory, then interpolates the y values to have same x values
simulation_results = vector_results_aggregator.vector_results_aggregator(csv_directory, parameter, simulations_seconds)
number_of_repetitions=simulation_results.shape[0]

y_mean = np.mean(simulation_results, axis=0)
moving_avg_y_values = simulation_results

for i in range(number_of_repetitions):
	moving_avg_y_values[i,:] = np.cumsum(simulation_results[i,:])
	moving_avg_y_values[i,:] = moving_avg_y_values[i,:] / np.arange(simulations_seconds + 1)[1:]


moving_avg_y_mean = y_mean
moving_avg_y_mean = np.cumsum(moving_avg_y_mean)
moving_avg_y_mean = moving_avg_y_mean/ np.arange(simulations_seconds + 1)[1:]
#print (moving_avg_y_values)

fig = plt.figure(1)

# Takes the parameter values from the Numpy Array


plt.xlabel("time")
plt.ylabel(parameter)

# Makes a 2D graph for each value of the parameter y, then puts it in the same figure.
# TODO how to set label for each graph? How to select the values of the other parameters for each y?
# using np.unique to extract only different values of y
#for y in np.unique(y_values):
#	# Selects the rows where the value of the column 1 (y) is = y
#	same_y = np_simulation_results[np_simulation_results[:,1]==y]
#	# Plots the x and z, assigning them a label to be displayed in the legend
#	plt.plot(same_y[:,0],same_y[:,2], label="%s = %s" %(y_parameter,y))

for i in range(number_of_repetitions):
	plt.plot(x_values, moving_avg_y_values[i,:], linewidth=0.3)

plt.plot(x_values, moving_avg_y_mean, label="mean", linewidth=3)

plt.legend(loc=2)
plt.title("S = 8 seconds")

plt.show()
