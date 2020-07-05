#
# This script aggregates results of vector files. 
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import vector_csv_parser
import os
import pandas as pd
import sys
import numpy as np

def vector_results_aggregator(dir_path, parameter, simulations_seconds):
	# Aggregates results parsing all csv files inside a folder
	filenames = next(os.walk(dir_path))[2]
	first_run = True
	
	# At wach run, we interpolate the vectors, in order to have same lenght vectors with same x values.
	# if response time, we have x files, x = number of repetitions. (The files are in the vector_CT_RT folder)
	# numpy.arange creates a vector of equally spaced numbers
	if (parameter == "ResponseTime" or parameter == "QueueLength"):
		for filename in filenames:
			results = vector_csv_parser.vector_csv_parser(dir_path+filename, parameter)

			if first_run == True:
				# At first run, creates the Dataframe from a pandas Series
				y_results = np.interp(np.arange(simulations_seconds), results[0,:], results[1,:])
				first_run = False
			else:
				# Then, concatenates all the remaining Series
				y_interp_values = np.interp(np.arange(simulations_seconds), results[0,:], results[1,:])
				y_results = np.append(y_results,y_interp_values, axis=0)
				#results = np.concatenate(results, vector_csv_parser.vector_csv_parser(dir_path+filename, "ResponseTime"), axis=0)
	else:
		print("ERROR: Ordinates available: ResponseTime - QueueLength")

	number_of_repetitions = len(filenames)
	y_results = np.reshape(y_results, (number_of_repetitions, simulations_seconds)) # I reshape them manually
	
	return y_results
	

	
## Main for testing
# TODO
