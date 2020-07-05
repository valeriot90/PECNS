#!/bin/bash
#
# This script finds simulations that have in common a value of a parameter. 
# The parameter and its value must be passed from command line as arguments.
# Also the path of the directory containig the simulations must be passed as parameter.
# Simulations found are then copied into a new folder, and the user can run the script again
# in this new folder with another parameter.
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

if [ "$#" -ne 3 ] 
then
    echo "USAGE: ./Script_Name  Parameter_Name Parameter_Value Path_Directory"
    exit 1
else
	# We retrieve the parameter name and its value, and the path of the directory
	parameter_name=$1
	parameter_value=$2
	path_source_dir=$3
	
	# We find simulations and we put their names in an array
	simulations=($(find ${path_source_dir} -maxdepth 1 -name "*-$parameter_name$parameter_value*"))
	# If at least one simulation is found, we create the result directory and we copy simulations 
	# found inside it
	if [ ${#simulations[@]} -eq 0 ]; 
	then
    	echo "No simulations found, sorry"
	else
		mkdir -p ${path_source_dir}/${parameter_name}${parameter_value}
   		for i in "${simulations[@]}"
		do
			cp $i ${path_source_dir}/${parameter_name}${parameter_value}
		done
		echo "Done, ${#simulations[*]} simulations found!"
	fi
fi
