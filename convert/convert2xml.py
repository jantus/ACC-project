#!/usr/bin/env python
#
# Converts one or more msh files to xml files.
# Using dolfin-convert.py by Anders Logg for file conversion.
# def gmsh2xml ( ifilename, ofilename ):
from dolfin_convert import gmsh2xml
from os import listdir
import os


path = '../naca_airfoil/msh/'

for in_file in listdir(path):
	file_path, file_extension = os.path.splitext(in_file)
	if file_extension == ".msh":
		in_file = path+in_file
		out_file = path+file_path+".xml"
		if os.path.isfile(out_file):
			print path+out_file + " already exists!"
			continue
	 	gmsh2xml(in_file, out_file)