#!/usr/bin/python
###############################################################################
#
# Name: generate_data.py
# Arguments (0):
# 	
# Output: 
# Example:
###############################################################################
import sys
import subprocess
import os

script_dir = "naca_airfoil"
###############################################################################
# Execute the run.sh script with the given parameters
# Arguments(0):
#	angle_start	: Smallest angle of attack (degrees)
#	angle_stop	: Largest agle of attack (degrees)
# 	n_angles	: Split angle_stop-angle_start in to n_angles parts
#	n_nodes		: number of nodes on one side of the airfoil
#	n_levels	: number of refinement steps in meshing  
# Return:
# 	Bool: indication of when it is ready.
###############################################################################

def run_script(angle_start, angle_stop, n_angles, n_nodes, n_levels):
	cwd = os.getcwd()
	os.chdir(script_dir)
	
	try: 
		print os.getcwd()
		print "$ ./run.sh", angle_start, angle_stop, n_angles, n_nodes, n_levels
		print "Loading..."
		subprocess.check_call(["./run.sh", angle_start, angle_stop, n_angles, n_nodes, n_levels])
	except subprocess.CalledProcessError:
		print "Oops: ./run.sh could not finish"
		return False
	except:
		print "Unexpected error:", sys.exc_info()[0]	
		return False
	os.chdir(cwd)
	return True
	


###############################################################################
# main loop
###############################################################################
angle_start = str(0)
angle_stop = str(30)
n_angles = str(10)
n_nodes = str(200)
n_levels = str(3)

if run_script(angle_start, angle_stop, n_angles, n_nodes, n_levels):
	print "Success: Data generated"
else:
	print "Failed: Data not generated"
