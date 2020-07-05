#
# This script plots the ECDF related to the RT.
# Abscissas are N*number_of_repetitions means of RT, ordinates are probabilities.
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
	

def plot_ecdf(dir_path, ordinate):
	means = retrieve_means(dir_path, ordinate)
	samples = np.sort(means)
	num_samples = len(samples)
	
	probabilities = []
	j=1
	for i in samples:
		probabilities = np.append(probabilities, j/num_samples)
		j=j+1
	
#	max_x_values = (2.54688, 2.5972299999999997, 2.6319999999999997, 2.66587, 2.66911, 2.67605, 2.6858299999999997, 2.69187, 2.6983599999999996, 2.70466, 2.71311, 2.71378, 2.7213700000000003, 2.72293, 2.7235400000000003, 2.73683, 2.74024, 2.7416400000000003, 2.7418299999999998, 2.75037, 2.7509900000000003, 2.7622400000000003, 2.76267, 2.76268, 2.76755, 2.7682900000000004, 2.77042, 2.77083, 2.7723, 2.7738, 2.7749099999999998, 2.77507, 2.7753799999999997, 2.77814, 2.7856099999999997, 2.78589, 2.78621, 2.78982, 2.79028, 2.79296, 2.79448, 2.79521, 2.79581, 2.79616, 2.7974, 2.79762, 2.80137, 2.80178, 2.80198, 2.80524, 2.80682, 2.8069599999999997, 2.80777, 2.80871, 2.80975, 2.81719, 2.81758, 2.81814, 2.8191200000000003, 2.8237799999999997, 2.8269900000000003, 2.83051, 2.83372, 2.8340099999999997, 2.83407, 2.83428, 2.83643, 2.83705, 2.8374900000000003, 2.83807, 2.83913, 2.84111, 2.84115, 2.8416200000000003, 2.8418900000000002, 2.84233, 2.84259, 2.84281, 2.84386, 2.84557, 2.84688, 2.8481099999999997, 2.8517200000000003, 2.85253, 2.85354, 2.8538799999999998, 2.8552299999999997, 2.85544, 2.85748, 2.85887, 2.8599200000000002, 2.86076, 2.86121, 2.86144, 2.86163, 2.8626099999999997, 2.86298, 2.86593, 2.87111, 2.87121, 2.87206, 2.87249, 2.87353, 2.87458, 2.87803, 2.87813, 2.88378, 2.88444, 2.88485, 2.8858099999999998, 2.88583, 2.88726, 2.88858, 2.8886, 2.88976, 2.8910400000000003, 2.89224, 2.89296, 2.89483, 2.8955, 2.89621, 2.8983, 2.8984099999999997, 2.89885, 2.89938, 2.8999200000000003, 2.90309, 2.90572, 2.90928, 2.90985, 2.91035, 2.9111599999999997, 2.91197, 2.91424, 2.91508, 2.9156400000000002, 2.9167, 2.91737, 2.91803, 2.92246, 2.92448, 2.92495, 2.92497, 2.92599, 2.9264, 2.9267, 2.92703, 2.92732, 2.92965, 2.92999, 2.93018, 2.93027, 2.93091, 2.93364, 2.93377, 2.93425, 2.93554, 2.93577, 2.93667, 2.9375299999999998, 2.93764, 2.93768, 2.93807, 2.93908, 2.93971, 2.94043, 2.94112, 2.94349, 2.94409, 2.94424, 2.94516, 2.94575, 2.94585, 2.9459299999999997, 2.94723, 2.9483599999999996, 2.95092, 2.9523599999999997, 2.9539, 2.95588, 2.95591, 2.96041, 2.96179, 2.9621, 2.96224, 2.96267, 2.96315, 2.96671, 2.96837, 2.96868, 2.9698900000000004, 2.96995, 2.97175, 2.97277, 2.97352, 2.97452, 2.97716, 2.9774599999999998, 2.97763, 2.97839, 2.97893, 2.97966, 2.98026, 2.9822599999999997, 2.98273, 2.98279, 2.98294, 2.98375, 2.98378, 2.98752, 2.98772, 2.98998, 2.98999, 2.9908200000000003, 2.9908900000000003, 2.99226, 2.99249, 2.99358, 2.99553, 2.9963, 2.99702, 3.0015400000000003, 3.00157, 3.00612, 3.00749, 3.0076400000000003, 3.00835, 3.00884, 3.0103299999999997, 3.01099, 3.01154, 3.0119700000000003, 3.01251, 3.01288, 3.01346, 3.0135400000000003, 3.01401, 3.01535, 3.01579, 3.01649, 3.0171200000000002, 3.0179099999999996, 3.02093, 3.02219, 3.0230799999999998, 3.02395, 3.0244, 3.0245599999999997, 3.02685, 3.02785, 3.02842, 3.02915, 3.03008, 3.0301099999999996, 3.0309, 3.03215, 3.03257, 3.03442, 3.03499, 3.03645, 3.03704, 3.03715, 3.03764, 3.03917, 3.0394200000000002, 3.03976, 3.04014, 3.04105, 3.0413900000000003, 3.04422, 3.04475, 3.0455400000000004, 3.04564, 3.0470599999999997, 3.04773, 3.05048, 3.05175, 3.05178, 3.05228, 3.0529900000000003, 3.05423, 3.0554, 3.0558099999999997, 3.05598, 3.05877, 3.06025, 3.06508, 3.06685, 3.06799, 3.0694, 3.0697200000000002, 3.0699099999999997, 3.0701099999999997, 3.07116, 3.07139, 3.07265, 3.0729, 3.07647, 3.0815799999999998, 3.08501, 3.08533, 3.08574, 3.0868, 3.08704, 3.08787, 3.0878900000000002, 3.08976, 3.09059, 3.09199, 3.09479, 3.09731, 3.0979099999999997, 3.09849, 3.10013, 3.10031, 3.10125, 3.10164, 3.10245, 3.10252, 3.10541, 3.10609, 3.10678, 3.10984, 3.11057, 3.11327, 3.11439, 3.11483, 3.1154900000000003, 3.11552, 3.11592, 3.11618, 3.11618, 3.11702, 3.11748, 3.1183400000000003, 3.11845, 3.1185099999999997, 3.11928, 3.12022, 3.1238200000000003, 3.12391, 3.12453, 3.12682, 3.1269299999999998, 3.1272, 3.12842, 3.12895, 3.12978, 3.13137, 3.1314, 3.13253, 3.13835, 3.13848, 3.13857, 3.13967, 3.14003, 3.14011, 3.14014, 3.14051, 3.14063, 3.14083, 3.14491, 3.14608, 3.14847, 3.14894, 3.1493599999999997, 3.15332, 3.15382, 3.15428, 3.15536, 3.15558, 3.15574, 3.15599, 3.15654, 3.15771, 3.1596599999999997, 3.16076, 3.16093, 3.16645, 3.16723, 3.16931, 3.17097, 3.17152, 3.1717299999999997, 3.1722099999999998, 3.1728099999999997, 3.1819, 3.18295, 3.18495, 3.18513, 3.18614, 3.1863900000000003, 3.18962, 3.19294, 3.1934299999999998, 3.1938299999999997, 3.19788, 3.2008, 3.20107, 3.20193, 3.20195, 3.20205, 3.20233, 3.20295, 3.2062, 3.20668, 3.20687, 3.20707, 3.2109400000000003, 3.2109900000000002, 3.21266, 3.2128799999999997, 3.21317, 3.21446, 3.21687, 3.2180299999999997, 3.2181900000000003, 3.21908, 3.21921, 3.22084, 3.2208799999999997, 3.22142, 3.22479, 3.2259599999999997, 3.22668, 3.22843, 3.23205, 3.23454, 3.23801, 3.23907, 3.2398, 3.2401400000000002, 3.24273, 3.24326, 3.24626, 3.2471200000000002, 3.24722, 3.24752, 3.25164, 3.25339, 3.25369, 3.25615, 3.26005, 3.2665, 3.27136, 3.27268, 3.27924, 3.2794800000000004, 3.2796, 3.28137, 3.2867800000000003, 3.2892699999999997, 3.29134, 3.29143, 3.29215, 3.29432, 3.29814, 3.29828, 3.30064, 3.30075, 3.30099, 3.30726, 3.30805, 3.31025, 3.3195699999999997, 3.3201699999999996, 3.32539, 3.3277099999999997, 3.32789, 3.3280199999999995, 3.32986, 3.3301, 3.33103, 3.3353599999999997, 3.33773, 3.33866, 3.3397699999999997, 3.34542, 3.3454300000000003, 3.3603099999999997, 3.3606800000000003, 3.3626, 3.36654, 3.37489, 3.3788300000000002, 3.4147800000000004, 3.4204, 3.42211, 3.44611, 3.4552, 3.45897, 3.46311, 3.4881900000000003, 3.4997599999999998, 3.5651599999999997, 3.5955800000000004, 3.6459099999999998, 3.72085, 3.7370400000000004, 3.93603)
#	np_max_x_values = np.array(max_x_values)
#	max_total_mean = 3.03974328
	
	np_probabilities = np.array(probabilities)
		
#	plt.step(np_max_x_values, np_probabilities, linewidth=1.5, color="blue", label="ECDF Max-Capacity")
#	plt.axvline(x=max_total_mean, linestyle="--", color="orange", label="Mean Max-Capacity")
	
	plt.step(samples, np_probabilities, linewidth=1.5, color="blue", label="ECDF")
	total_mean = np.mean(samples)
	plt.axvline(x=total_mean, linestyle="--", color="red", linewidth=1.5, label="mean")
	
	
	plt.grid(True)
	title = "t=5s, X=5%, S=0.2s"
	plt.title(title)
	plot_margin = 0.01
	x0, x1, y0, y1 = plt.axis()
	plt.axis((x0 - plot_margin, x1 + plot_margin, y0 - plot_margin, y1 + plot_margin))
	plt.xlabel("responseTime")
	plt.ylabel("probability")
	plt.legend(loc=4)
	
	plt.show()
	
	return probabilities
	
	
# Main for testing
if len(sys.argv) == 3:	
	print(plot_ecdf(sys.argv[1], sys.argv[2]))
else:
	print("USAGE: script_name path_dir_csv_with_final_slash ordinate")
	sys.exit()

