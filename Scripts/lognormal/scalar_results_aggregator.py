#
# This script aggregates results parsing all .sca.csv files inside a folder using the scalar_csv_parser, in
# a single table.
# Then fills another table using as ordinate and abscissa(s) two (three) parameters passed as 
# arguments, grouping results by parameters and making the mean for the ones with the same
# parameters 
#
# Example of a print *before* grouping results (parameters: X t responseTime)
#       X    k  switchTime    t  responseTime
#0    0.0  2.0         0.5  1.0       2.00821
#0    0.0  2.0         0.5  2.0       1.57100
#0    0.0  2.0         0.5  3.0       1.38702
#0    0.0  2.0         0.5  4.0       1.28843
#0    0.0  2.0         0.5  5.0       1.22397
#0  100.0  2.0         0.5  1.0       2.54053
#0  100.0  2.0         0.5  2.0       2.43664
#0  100.0  2.0         0.5  3.0       2.46104
#0  100.0  2.0         0.5  4.0       2.57398
#0  100.0  2.0         0.5  5.0       2.68662
#0   10.0  2.0         0.5  1.0       2.01393
#0   10.0  2.0         0.5  2.0       1.57095
#0   10.0  2.0         0.5  3.0       1.40728
#0   10.0  2.0         0.5  4.0       1.30504
#0   10.0  2.0         0.5  5.0       1.25355
#0    0.0  2.0         0.5  1.0       2.00613
#0    0.0  2.0         0.5  2.0       1.56902
#0    0.0  2.0         0.5  3.0       1.39128
#0    0.0  2.0         0.5  4.0       1.28151
#0    0.0  2.0         0.5  5.0       1.21557
#....
#
# Example of a pring *after* grouping results (parameters: X t responseTime)
#        X    t  responseTime
#0     0.0  1.0      2.000901
#1     0.0  2.0      1.564188
#2     0.0  3.0      1.381880
#3     0.0  4.0      1.282796
#4     0.0  5.0      1.215043
#5    10.0  1.0      1.995644
#6    10.0  2.0      1.570708
#7    10.0  3.0      1.395038
#....
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import scalar_csv_parser
import compute_CI
import os
import pandas as pd
import sys
import numpy as np

def scalar_results_aggregator(dir_path, *args):
	# Aggregates results parsing all csv files inside a folder
	filenames = next(os.walk(dir_path))[2]
	first_run = True
	last_parameter = args[-1][-1]
	repetitions = 500

	if last_parameter == "responseTime" or last_parameter == "packetReceived" or last_parameter == "numSwitch" or last_parameter == "queueLength":	
		
		for filename in filenames:
			if first_run == True:
				# At first run, creates the Dataframe from a pandas Series
				results = pd.DataFrame(scalar_csv_parser.scalar_csv_parser(dir_path+filename, last_parameter))
				first_run = False
			else:
				# Then, concatenates all the remaining Series
				results = pd.concat([results, scalar_csv_parser.scalar_csv_parser(dir_path+filename, last_parameter)])
		
		

		#orders results, 
		results.sort_values(['X', 'mk', 'mt', 'switchTime', 'wk', 'wt', last_parameter],inplace = True)

		#transform into numpy matrix
		np_results = results.as_matrix()
		number_of_scenarios= int(results.shape[0]/repetitions)

		#dtype = np.dtype([('X', float), ('k', float), ('switchTime', float), ('t', float), (last_parameter, float), ('CI', float)])

		
		CI_average_matrix = np.zeros((number_of_scenarios, 8))

		#Now we calculate the Confidence Interval for each scenario, and we add it next to the scenario's values. 
		for i in range (0, int(number_of_scenarios)):  #number of scenarios
			CI_average_matrix[i,:6] = np_results[i*repetitions, :6]
			CI_average_matrix[i, 6] = np.mean(np_results[i*repetitions:(i+1)*repetitions,6])
			CI_average_matrix[i, 7] = compute_CI.compute_CI_from_array(np_results[i*repetitions:(i+1)*repetitions,6], 99)

		#print (CI_average_matrix)

		# Groups results by indexes and makes the mean for the ones with the same indexes
#		if len(*args) == 2:
#			x = args[0][0]
#			y = args[0][1]
#			grouped_results = results.groupby([x])[y].mean()
#			grouped_results = grouped_results.reset_index()
#		elif len(*args) == 3:
#			x = args[0][0]
#			y = args[0][1]
#			z = args[0][2]
#			grouped_results = results.groupby([x,y])[z].mean()
#			grouped_results = grouped_results.reset_index()
#		else:
#			pass

	elif (sys.argv[3] or sys.argv[4] == "numSwitch"):
		# TODO
		print("To be implemented")
	elif (sys.argv[3] or sys.argv[4] == "queueLength"):
		# TODO
		print("To be implemented")
	elif (sys.argv[3] or sys.argv[4] == "packetReceived"):
		# TODO
		print("To be implemented")
	else:
		print("ERROR: Ordinates available: responseTime - packetReceived - numSwitch - queueLength")
		sys.exit()

	# Tells pandas to print all rows till 1000
	#pd.set_option('display.max_rows', 1000)
	
	#CI_average_matrix.dtype.names = 'X', "k", 'switchTime', 't', last_parameter, 'CI'
	#CI_average_matrix = np.array(CI_average_matrix, dtype=dtype)


	#print (CI_average_matrix)

	return CI_average_matrix
	

	
## Main for testing
#if (len(sys.argv) < 4 or len(sys.argv) > 5):
#	print("USAGE: script_name path_dir_csv_with_final_slash <X parameter name> <Y parameter name> [<Z parameter name>]")
#	sys.exit
#else:
#	print(scalar_results_aggregator(sys.argv[1], sys.argv[2:]))
