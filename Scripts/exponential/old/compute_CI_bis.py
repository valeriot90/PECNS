#
# This script returns the CI related to the RT
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import pandas as pd
import numpy as np
import os
import sys
import math
from scipy.stats import norm

def retrieve_means(dir_path, ordinate):
	means = []
	filenames = next(os.walk(dir_path))[2]
	
	for filename in filenames:
		csv_file = pd.read_csv(dir_path+filename)
		csv_file.drop(csv_file.columns[[0,1,2,3]], axis=1, inplace=True)
		csv_file = csv_file.ix[4:]
		np_csv_file = csv_file.as_matrix()
		means = np.append(means, csv_file)

	return means
	

def compute_CI(dir_path, ordinate, confidence_level):
	samples = retrieve_means(dir_path, ordinate)
	num_samples = len(samples)
	square_root_num_samples = math.sqrt(num_samples)
	sample_variance = np.var(samples)
	standard_deviation = math.sqrt(sample_variance)
	alfa_2 = norm.ppf(int(confidence_level)/100)
	
	confidence_interval = (standard_deviation/square_root_num_samples)*alfa_2
	
	return confidence_interval
	
		
	
# Main for testing
if len(sys.argv) == 4:	
	print(compute_CI(sys.argv[1], sys.argv[2], sys.argv[3]))
else:
	print("USAGE: script_name path_dir_csv_with_final_slash ordinate confidence_level_in_percentage")
	sys.exit()

