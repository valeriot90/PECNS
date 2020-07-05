#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#


import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

def retrieve_means(dir_path, ordinate):
	means = []
	filenames = next(os.walk(dir_path))[2]
	
	for filename in filenames:
		csv_file = pd.read_csv(dir_path+filename)
		csv_file.drop(csv_file.columns[[0,1,2,3]], axis=1, inplace=True)
		csv_file = csv_file.ix[6:]
		means = np.append(means, csv_file)
#		print(means)
	
	return means
	
	
def plot_epdf(dir_path, ordinate):
	num_bins = 15

	samples = retrieve_means(dir_path, ordinate)
	n, bins, patches = plt.hist(samples, num_bins, facecolor="green", alpha=0.75)

	total_mean = np.mean(samples)
	plt.axvline(x=total_mean, linestyle="--", color="red", linewidth=1.8, label="mean")
	
	median = np.median(samples)
	plt.axvline(x=median, linestyle="--", color="blue", linewidth=1.8, label="median")

	plt.grid(True)
	title = "t=5s, X=5%, S=0.2s"
	plt.title(title)
#	plot_margin = 0.01
#	x0, x1, y0, y1 = plt.axis()
#	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	plt.xlabel("responseTime")
	plt.ylabel("frequency")
	plt.legend(loc=1)

	plt.show()
	
	
	
# Main for testing
if len(sys.argv) == 3:	
	print(plot_epdf(sys.argv[1], sys.argv[2]))
else:
	print("USAGE: script_name path_dir_csv_with_final_slash ordinate")
	sys.exit()
