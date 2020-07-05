#
# This script plots a 2D/3D graph, depending on the number of arguments
# Data are fetched from files .sca.csv contained in a folder
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import scalar_results_aggregator_bis
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
	x_parameter=sys.argv[2]
	y_parameter=sys.argv[3]
elif len(sys.argv) == 5:
	x_parameter=sys.argv[2]
	y_parameter=sys.argv[3]
	z_parameter=sys.argv[4]
else:
	print("USAGE: script_name path_dir_csv_with_final_slash <X parameter name> <Y parameter name> [<Z parameter name>]")
	sys.exit()

csv_directory = sys.argv[1]
parameters = sys.argv[2:]
print(parameters)

# Aggregates csv files in the directory, grouping results by parameters and making the mean for the ones with the same
# parameters 
simulation_results = scalar_results_aggregator_bis.scalar_results_aggregator(csv_directory, parameters)

# Converts from pandas DataFrame tu Numpy Array
np_simulation_results = simulation_results.as_matrix()

# 2D plot
if len(parameters) == 2:
	x_values = np_simulation_results[:,0]
	y_values = np_simulation_results[:,1]
	
	print(x_values)
	print(y_values)
	
#	max_x_values = (0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1)
#	max_y_values = (2.87301658 ,2.88161154,2.89014332,2.89845578,2.90578972,2.91182566,2.92121216,2.93175474,2.93970294,2.9492261)
##	max_errors = (0.02,0.022,0.024,0.028,0.034,0.094,0.35)		# max_1
##	single_errors = (0.34,0.34,0.34,0.34,0.34,0.34,0.34)
#	rand_errors = (3.9,4,4.2,4.4,4.3,4.6,4.8,5.1,5.1,5.3)
#	max_errors = (0.018,0.018,0.018,0.018,0.018,0.018,0.018,0.018,0.018,0.018)		# max 2
	
	plt.xlabel(x_parameter)
	plt.ylabel(y_parameter)
	
#	plt.errorbar(x_values, y_values, rand_errors, linewidth=1.5, color='black')
#	plt.errorbar(max_x_values, max_y_values, max_errors, linewidth=1.5, color='black')
	
	plt.plot(x_values, y_values, label='Random Algorithm', color='green', linewidth=1.5, marker='s', markersize='7')
#	plt.plot(max_x_values, max_y_values, label='Max-Capacity Algorithm', linewidth=1.5, marker='o', markersize='7')
	
	plt.legend(loc=2)
	plt.grid(True)
#	plot_margin = 0.1
#	x0, x1, y0, y1 = plt.axis()
#	plt.axis((x0+plot_margin, x1+plot_margin, y0, y1))
	
	title = "t = 5 seconds - X = 5%"
	plt.title(title)
	

# 3D plot
elif len(parameters) == 3:
#	fig = plt.figure(1)

#	# Assigns to ax a 3d Axes instance
#	ax = fig.gca(projection='3d')
	# Takes the parameter values from the Numpy Array
	x_values = np_simulation_results[:,0]
	y_values = np_simulation_results[:,1]
	z_values = np_simulation_results[:,2]

#	# Plots a trisurface on the axes. cmap is the color map
#	ax.plot_trisurf(x_values, y_values, z_values, cmap=cm.jet, linewidth=0.2)

#	# Sets the label names
#	ax.set_xlabel(x_parameter)
#	ax.set_ylabel(y_parameter)
#	ax.set_zlabel(z_parameter)

	# Says that now we are furking on figure 2
	plt.figure(2)
	plt.xlabel(x_parameter)
	plt.ylabel(z_parameter)

	# Makes a 2D graph for each value of the parameter y, then puts it in the same figure.
	# TODO how to set label for each graph? How to select the values of the other parameters for each y?
	# using np.unique to extract only different values of y
	cmap = plt.get_cmap('Set1')
	N = 15
	i=0
	markers = ('^', 'p', 'o', "v", "s", "H", ".", "8") 
	# CI matrix filled manually for each simulation....a row corresponds to a set of CI of the same curve
	CI_matrix = [[6, 0.6, 0.34, 0.38, 0.36, 0.44],
				 [6, 0.6, 0.34, 0.38, 0.36, 0.44],
				 [6, 0.6, 0.34, 0.38, 0.36, 0.44],
				 [6, 0.6, 0.34, 0.38, 0.36, 0.44],
				 [6, 0.6, 0.34, 0.38, 0.36, 0.44]]
	for y in np.unique(y_values):
		color = cmap(float(i)/N)
		# Selects the rows where the value of the column 1 (y) is = y
		same_y = np_simulation_results[np_simulation_results[:,1]==y]
		# Plots the x and z, assigning them a label to be displayed in the legend
		plt.plot(same_y[:,0],same_y[:,2], label="%s = %s" %("S",y), c=color, linewidth=1.5, marker=markers[i%8])
		plt.errorbar(same_y[:,0],same_y[:,2], CI_matrix[i], color="black", linewidth=1.5)
		# Plots the x and z, assigning them a label to be displayed in the legend
		plt.plot(same_y[:,0],same_y[:,2], marker = markers[i%8], c=color, markersize=7)
		plt.grid(True)
		i=i+1
	j=0	
	plt.legend(loc=1)
	plt.xticks(np.arange(0, max(same_y[:,0])+5, 5.0))
	plot_margin = 1.5
	x0, x1, y0, y1 = plt.axis()
	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	plt.title("X = 100%")
else:
	print (simulation_results)

plt.show()




print(np_simulation_results)
