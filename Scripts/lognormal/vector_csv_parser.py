#
# This script parses (and prints) a .csv file related to a .vec file (generated with csv_generator.sh)
#
# Example of a print:
#                 0         1         2         3         4         5      
#Time          2.074483  2.095021  2.100148  2.143839  2.185871  2.191339   .... 
#ResponseTime  2.074480  2.095020  2.100150  2.143840  2.185870  2.191340
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import pandas as pd
import sys

def vector_csv_parser(filename, ordinate):
	# Reads a csv file
	vec_csv_file = pd.read_csv(filename)
	
	# Defines an index	
	if ordinate == "ResponseTime":
		# Transposes the pandas array, so the index is the first row, the values the second
		vec_csv_file = vec_csv_file.transpose()
		vec_csv_file.index = ["Time", "ResponseTime"]
	
	elif ordinate == "QueueLength":
		# Transposes the pandas array, so the index is the first row, the values the second
		vec_csv_file = vec_csv_file.transpose()
		vec_csv_file.index = ["Time", "QueueLength"]
	
	else:
		print("ERROR: Ordinates available: ResponseTime - QueueLength")

	np_vec_csv_file = vec_csv_file.as_matrix()


	return np_vec_csv_file
	

	
## Main for testing
#if len(sys.argv) == 3:	
#	print(vector_csv_parser(sys.argv[1], sys.argv[2]))
#else:
#	print("USAGE: script_name path_file_csv ordinate")
#	sys.exit()

