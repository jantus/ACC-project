#!/usr/bin/python
###############################################################################
#
# Name: generate_data.py
# Arguments (0):
# 	
# Output: 
# Example:
###############################################################################
from dolfin_convert import gmsh2xml
import os
import sys

path = "../naca_airfoil/msh/"

###############################################################################
# Converts all files form .msh to .xml in the give directory. 
#	deletes all msh. files when done
# Arguments (0):
# 	path: path do directory	
###############################################################################
def convert_files_at_path(path):
	for in_file in os.listdir(path):
		file_path, file_extension = os.path.splitext(in_file)
		if file_extension == ".msh":
			in_file = path+in_file
			out_file = path+file_path+".xml"
			if os.path.isfile(out_file):
				print path+out_file + " already exists!"
			else:
				gmsh2xml(in_file, out_file)

			if os.path.isfile(in_file):
				try:
					os.remove(in_file)
				except : 
					print "Could not remove "+str(in_file)+" due to unexpected error:", sys.exc_info()[0]



