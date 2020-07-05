#!/bin/bash
#
# This script generates .csv files from .sca and .vec files that are in a directory.
# The path of the directory must be passed from command line as first argument.
#
# Authors: Alberto Cristallo, Luca Ciampi, Valerio Tanferma
#

if [ "$#" -ne 1 ] 
then
    echo "USAGE: ./Script_Name  Path_Directory"
    exit 1
else
	# We retrieve the path of the directory (it is the first argument)
	path_dir=$1
	# This is the name of the root directory that will contain .csv files (if they will be generated)
	root_directory="csv"
	
	# We check if at least one .sca file exists in the directory
	count=`ls -1 ${path_dir}/*.sca 2>/dev/null | wc -l`
	if [ $count != 0 ]
	then 
		# We create .csv containing X,k,t,S -> queueLengthMax for each aircraft
		for f in ${path_dir}/*.sca
		do
	  		scavetool scalar -p "name(\"X\") OR name(\"k\") OR name(\"t\") OR name(\"switchTime\") OR name(\"queueLength:max\")" -O $f.csv -F csv $f
		done	
		mkdir -p ${path_dir}/${root_directory}/scalar_queueLength
		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/scalar_queueLength
		
		# We create .csv containing X,k,t,S -> numSwitchSum for each aircraft
		for f in ${path_dir}/*.sca
		do
	  		scavetool scalar -p "name(\"X\") OR name(\"k\") OR name(\"t\") OR name(\"switchTime\") OR name(\"numSwitch:sum\")" -O $f.csv -F csv $f
		done	
		mkdir -p ${path_dir}/${root_directory}/scalar_numSwitch
		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/scalar_numSwitch
		
		# We create .csv containing X,k,t,S -> ResponseTimeMean for each aircraft
		for f in ${path_dir}/*.sca
		do
			scavetool scalar -p "name(\"X\") OR name(\"k\") OR name(\"t\") OR name(\"switchTime\") OR name(\"responseTime:mean\")" -O $f.csv -F csv $f
		done
		mkdir -p ${path_dir}/${root_directory}/scalar_responseTime
		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/scalar_responseTime
		
		# We create .csv containing X,k,t,S -> PacketReceivedSum (one for N aircrafts)
		for f in ${path_dir}/*.sca
		do
			scavetool scalar -p "name(\"X\") OR name(\"k\") OR name(\"t\") OR name(\"switchTime\") OR name(\"packetReceived:sum\")" -O $f.csv -F csv $f
		done
		mkdir -p ${path_dir}/${root_directory}/scalar_packetReceived
		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/scalar_packetReceived
		
		echo "Files .csv for files .sca generated"
	else
		echo "No files .sca in this directory"
	fi
	
	# We check if at least one .vec file exists in the directory
	count=`ls -1 ${path_dir}/*.vec 2>/dev/null | wc -l`
	if [ $count != 0 ]
	then 
#		# We create a .csv for each aircraft containing TimeStamp -> ResponseTime
#		for f in ${path_dir}/*.vec
#		do
#			for i in {0..50}
#			do
#				scavetool vector -p "module(AerocomSystem.airCraft[$i]) AND name(\"responseTime:vector\")" -O $f.aircraft$i.csv -F csv $f
#			done
#		done
#		mkdir -p ${path_dir}/${root_directory}/vector_aircrafts_RT
#		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/vector_aircrafts_RT
		
		# We create a .csv for each aircraft containing TimeStamp -> QueueLength
		for f in ${path_dir}/*.vec
		do
			for i in {0..50}
			do
				scavetool vector -p "module(AerocomSystem.airCraft[$i]) AND name(\"queueLength:vector\")" -O $f.aircraft$i.csv -F csv $f
			done
		done	
		mkdir -p ${path_dir}/${root_directory}/vector_aircrafts_QL
		mv ${path_dir}/*.csv ${path_dir}/${root_directory}/vector_aircrafts_QL
		
		echo "Files .csv for files .vec generated"
	else
		echo "No files .vec in this directory"
	fi
fi
