#!/usr/bin/python
###############################################################################
#
# Name: lift_to_drag_ratio.py
# Arguments (0):
# 	
# Output: 
# Example:
###############################################################################
import os

###############################################################################
# Reads given .m file and returns the content as a list
# where each element is a row.
# Arguments:
#	filepath: Path o the file
###############################################################################
def get_data_from_file(filepath):
	path = "naca_airfoil/navier_stokes_solver/results/"
	filename = "drag_ligt.m"

	content_list = []
	if os.isfile(filepath):
		f = open(filepath, "r")
		file_content = f.read()
		content_list = file_content.split("\n")

	return content_list[1:]


###############################################################################
# Calculate lift to drag ratio for each element in the list
# 
# Arguments(1):
#	data_list: string list wher each element consist of "time lift, drag" 
# Return:
#	tuple list of (time, lift/drag) for each element in data_list 
###############################################################################
def calculate_lift_to_drag_ratio(data_list):
	result_list = []
	for line in content_list:
		element = line.split("\t")
		if len(element) < 3:
			continue
		result_list.append((float(element[0]), float(element[1])/float(element[2])))
	return result_list




