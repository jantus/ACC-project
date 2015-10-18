import os
from generate_data import run_script
from generate_data import airfoil
from convert2xml import convert_files_at_path as convert

def main():
	# Go to the right directory
	cwd = os.getcwd()
	os.chdir("../naca_airfoil") 
	
	# run script
	angle_start = str(0)
	angle_stop = str(30)
	n_angles = str(10)
	n_nodes = str(200)
	n_levels = str(3)

	run_script(angle_start, angle_stop, n_angles, n_nodes, n_levels)

	## convert files
	convert("msh/") 	

	num_samples = str(10)
	visc = str(0.0001)
	speed = str(10)
	T = str(1)

	## run airfoul
	os.chdir("navier_stokes_solver")
	path = "../msh/"
	for data_file in os.listdir(path):
		file_path, extension = os.path.splitext(data_file) 
		if extension == ".xml":
			data_file = path+data_file
			## start new worker
			airfoil(num_samples, visc, speed, T, data_file)

if __name__ == "__main__":
	main()
