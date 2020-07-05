#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#


import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy import stats

def retrieve_means(dir_path, ordinate):
	means = []
	filenames = next(os.walk(dir_path))[2]
	
	for filename in filenames:
		csv_file = pd.read_csv(dir_path+filename)
		csv_file.drop(csv_file.columns[[0,1,2,3]], axis=1, inplace=True)
		csv_file = csv_file.ix[6:]
		means = np.append(means, csv_file)
	
	return means
	
	
def qq_plot(dir_path, ordinate):
	samples = retrieve_means(dir_path, ordinate)
	std = np.std(samples)
	
	
	a, b = stats.probplot(samples, dist=stats.lognorm(std), plot=plt)

	print(std)
	plt.grid(True)
	title = "t=5s, X=5%, S=0.2s"
	plt.title(title)
#	plot_margin = 0.01
#	x0, x1, y0, y1 = plt.axis()
#	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	plt.xlabel("theorical distribution quantiles")
	plt.ylabel("quantiles")
	plt.text(1.3, 2.6, "R^2 = %f"%(b[2]**2), fontsize=14)
	#plt.()
	#plt.legend(loc=2)

	plt.show()
	
	
	
# Main for testing
if len(sys.argv) == 3:	
	print(qq_plot(sys.argv[1], sys.argv[2]))
else:
	print("USAGE: script_name path_dir_csv_with_final_slash ordinate")
	sys.exit()
