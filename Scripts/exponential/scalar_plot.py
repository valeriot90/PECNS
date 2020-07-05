#
# This script plots a 2D/3D graph, depending on the number of arguments
# Data are fetched from files .sca.csv contained in a folder
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import scalar_results_aggregator
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter

#numbers correspond to the column in wich are the values of the parameter


name_par = dict(X = 0, k = 1, switchTime = 2, t = 3, average = 4, CI = 5)

# Checks the number of the input parameters, assigns the parameters to variables.
# 2 parameters = 2D plot (x,y)     3 parameters = 3D plot (x,y,z) (or multiple lines on 2D plot, (x-y,z))
if len(sys.argv) == 4:
	x_parameter=sys.argv[2]
	y_parameter=sys.argv[3]
	
	x_par_col= name_par[sys.argv[2]]
	y_par_col=4
elif len(sys.argv) == 5:
	x_parameter=sys.argv[2]
	y_parameter=sys.argv[3]
	z_parameter=sys.argv[4]
	
	x_par_col= name_par[sys.argv[2]]
	y_par_col=name_par[sys.argv[3]]
	z_par_col=4
else:
	print("USAGE: script_name path_dir_csv_with_final_slash <X parameter name> <Y parameter name> [<Z parameter name>]")
	sys.exit()

csv_directory = sys.argv[1]
parameters = sys.argv[2:]
print(x_par_col, y_par_col, z_par_col)
# Aggregates csv files in the directory, grouping results by parameters and making the mean for the ones with the same
# parameters 
simulation_results = scalar_results_aggregator.scalar_results_aggregator(csv_directory, parameters)

# Converts from pandas DataFrame tu Numpy Array
#np_simulation_results = simulation_results.as_matrix()

# 2D plot
if len(parameters) == 2:
	x_values = simulation_results[:,x_par_col]
	y_values = simulation_results[:,y_par_col]
	plt.xlabel(x_parameter)
	plt.ylabel(y_parameter)
	plt.plot(x_values, y_values, x_values, y_values, 'bo', markersize=10, linewidth=1.5)
	plt.grid(True)
	plot_margin = 1.5
	x0, x1, y0, y1 = plt.axis()
	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	#title = "Correlation between the parameter %s and the parameter %s" % (x_parameter, y_parameter)
	#plt.title(title)

# 3D plot
elif len(parameters) == 3:
	# Takes the parameter values from the Numpy Array
	x_values = simulation_results[:,x_par_col]
	y_values = simulation_results[:,y_par_col]
	z_values = simulation_results[:,z_par_col]

	#fig = plt.figure(1)

	# Assigns to ax a 3d Axes instance
	#ax = fig.gca(projection='3d')

	# Plots a trisurface on the axes. cmap is the color map
	#ax.plot_trisurf(x_values, y_values, z_values, cmap=cm.jet, linewidth=0.2)

	# Sets the label names
	#ax.set_xlabel(x_parameter)
	#ax.set_ylabel(y_parameter)
	#ax.set_zlabel(z_parameter)

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
	for y in np.unique(y_values):
		i=i+1
		color = cmap(float(i)/N)

		# Selects the rows where the value of the column 1 (y) is = y
		same_y = simulation_results[simulation_results[:,y_par_col]==y]
		print (same_y)
		# Plots the x and z, assigning them a label to be displayed in the legend
		#plt.plot(same_y[:,x_par_col],same_y[:,z_par_col], label="%s = %s" %(y_parameter,y), c=color, linewidth=1.5, marker=markers[i%8])
		# Plots the x and z, assigning them a label to be displayed in the legend
	#	plt.plot(same_y[:,x_par_col],same_y[:,z_par_col], label="%s = %s" %("S",y), c=color, linewidth=1.5, marker=markers[i%8])
		plt.errorbar(same_y[:,x_par_col], same_y[:,z_par_col], same_y[:,name_par["CI"]],color="black", linewidth=1.5)
		plt.plot(same_y[:,x_par_col],same_y[:,z_par_col], marker = markers[i%8], c=color, markersize=5, linewidth=1.5, label="%s = %s" %("S",y))
		
	plt.grid(True)
	plt.legend(loc=2)
	plot_margin = 1.5
	x0, x1, y0, y1 = plt.axis()
	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	plt.title("t = 5 seconds")
else:
	#print (simulation_results)
	pass

plt.show()




print(simulation_results)
