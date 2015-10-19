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
	content_list = []
	if os.path.isfile(filepath):
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
	for line in data_list:
		element = line.split("\t")
		if len(element) < 3:
			continue
		result_list.append((float(element[0]), float(element[1])/float(element[2])))
	return result_list



###############################################################################
# Finds the largest lift to drag ratio in a list
# 
# Arguments(1):
#	lift_to_drag_list: list (time, lift_to_drag_ratio)
# Return:
#	(time, lift_to_drag_ratio)	
###############################################################################
def max_lift_to_drag_ratio(lift_to_drag_list):
	return max(lift_to_drag_list, key=lambda item:item[1])

###############################################################################
# Finds the average lift to drag of list
# 
# Arguments(1):
#	lift_to_drag_list: list (time, lift_to_drag_ratio)
# Return:
#	average_lift_to_drag_ratio
###############################################################################
def average_lift_to_drag_ratio(lift_to_drag_list):
	return sum([element[1] for element in lift_to_drag_list])/len(lift_to_drag_list)



###############################################################################
# main loop
###############################################################################
path = "naca_airfoil/navier_stokes_solver/results/"
filename = "drag_ligt.m"
data_list = get_data_from_file(path+filename)
lift_to_drag_list = calculate_lift_to_drag_ratio(data_list)
print "max:",max_lift_to_drag_ratio(lift_to_drag_list)
print "average:", average_lift_to_drag_ratio(lift_to_drag_list)

