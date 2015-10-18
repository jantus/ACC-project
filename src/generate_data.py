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
	try: 
		print "$ ./run.sh", angle_start, angle_stop, n_angles, n_nodes, n_levels
		print "Loading..."
		subprocess.check_call(["./run.sh", angle_start, angle_stop, n_angles, n_nodes, n_levels])
	except subprocess.CalledProcessError:
		print "Oops: ./run.sh could not finish"
		return False
	except:
		print "Unexpected error:", sys.exc_info()[0]	
		return False
	return True
	


###############################################################################
# Execute the airfoil binary
# Arguments(5):
#	num_samplse	: Number of samplse
#	visc		: The viscosity
#	spped		: The speed of the aircraft in m/s
#	T		: Total time
#	mesh 		: Path to a mesh file
# Return:
###############################################################################

def airfoil(num_samples, visc, speed, T, mesh):
	try: 
		print "$ ./airfoil", num_samples, visc, speed, T, mesh
		print "Loading..."
		subprocess.check_call(["./airfoil", num_samples, visc, speed, T, mesh])
	except subprocess.CalledProcessError:
		print "Oops: ./airfoil could not finish"
		return False
	except:
		print "Unexpected error:", sys.exc_info()[0]	
		return False
	return True
	

