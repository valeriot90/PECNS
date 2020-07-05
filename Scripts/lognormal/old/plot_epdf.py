#
# This script plots the EPDF related to the RT.
# Abscissas are N*number_of_repetitions means of RT, ordinates are probabilities.
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

def retrieve_means(dir_path, ordinate):
	means = []
	filenames = next(os.walk(dir_path))[2]
	
	for filename in filenames:
		csv_file = pd.read_csv(dir_path+filename)
		csv_file.drop(csv_file.columns[[0,1,2,3]], axis=1, inplace=True)
		csv_file = csv_file.ix[4:]
		means = np.append(means, csv_file)
	
	return means
	

def plot_epdf(dir_path, ordinate):
	samples = retrieve_means(dir_path, ordinate)
	num_samples = len(samples)
	number_bins = num_samples/10
	
	p, x = np.histogram(samples, bins=number_bins)
	x = x[:-1] + (x[1] - x[0])/2   # convert bin edges to centers
#	f = UnivariateSpline(x, p, s=number_bins)	# We try with two values of s, s=smoothing factor
	f = UnivariateSpline(x, p, s=num_samples)
	plt.plot(x, f(x), linewidth=1.5)
	plt.grid(True)
	title = "Empirical PDF"
	plt.title(title)
	plt.xlabel("Response Time")
	plt.ylabel("Probability Density")	
	total_mean = np.mean(samples)
	plt.axvline(x=total_mean, linestyle="--", color="red")
	
	plt.show()
	
	return 0
	
	
# Main for testing
if len(sys.argv) == 3:	
	print(plot_epdf(sys.argv[1], sys.argv[2]))
else:
	print("USAGE: script_name path_dir_csv_with_final_slash ordinate")
	sys.exit()

