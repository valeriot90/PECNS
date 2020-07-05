#
# This script parses (and prints) a .csv file related to .sca file (generated with csv_generator.sh)
#
# Example of a print:
#      X    k  switchTime    t  responseTime
#0  10.0  0.5         3.0  1.0       2233.94
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import pandas as pd
import numpy as np
import sys

def scalar_csv_parser(filename, ordinate):
	# Reads a csv file
	sca_csv_file = pd.read_csv(filename)
	# Eliminates columns we are not interested in
	sca_csv_file.drop(sca_csv_file.columns[[0,1,2,3]], axis=1, inplace=True)
	
	if ordinate == "packetReceived":
		pass
		
	# We have values for each aircrafts, so we compute the mean of these values
	elif ordinate == "queueLength" or ordinate == "numSwitch" or ordinate == "responseTime":
		#sca_csv_file.iloc[4]  = sca_csv_file.iloc[4:].mean() 
		repetition_matrix = sca_csv_file.iloc[:5].copy()
		model_row = sca_csv_file.iloc[:5].copy()

		# Transposes the pandas array, so the index is the first row, the values the second
		repetition_matrix = repetition_matrix.transpose()
		model_row = model_row.transpose()

		for i in range(5, sca_csv_file.shape[0]):
			model_row[4] = sca_csv_file.iloc[i]
			repetition_matrix = pd.concat([repetition_matrix,model_row])





	else:
		print("ERROR: Ordinates available: responseTime - packetReceived - queueLength - numSwitch")	

	


	# Defines an index	
	#sca_csv_file.index = ["X", "k", "switchTime", "t", ordinate]

	# Resets the index
	#sca_csv_file = sca_csv_file.reset_index(drop=True)
	repetition_matrix.columns = ['X', 'k', 'switchTime', 't', ordinate]

	repetition_matrix = repetition_matrix.reset_index(drop=True)


	return repetition_matrix
	
	
	
## Main for testing
#if len(sys.argv) == 3:	
#	print(scalar_csv_parser(sys.argv[1], sys.argv[2]))
#else:
#	print("USAGE: script_name path_file_csv ordinate")
#	sys.exit()

