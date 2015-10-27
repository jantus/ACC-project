import os
from generate_data import run_script
from convert2xml import convert_files_at_path as convert
from generate_data import airfoil
from plot_result import plot_result

def main():
	# Go to the right directory
	cwd = os.getcwd()
	os.chdir("../naca_airfoil") 
	
	# run script
	angle_start = str(0)
	angle_stop = str(30)
	n_angles = str(1)
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
	path = "../msh/"
	os.chdir("navier_stokes_solver/") 
	result_list = []
	for data_file in os.listdir(path):
		print os.getcwd()
		file_path, extension = os.path.splitext(data_file) 
		if extension == ".xml":
			## start new worker
			print data_file
			airfoil(num_samples, visc, speed, T, path+data_file)
			f = open('results/drag_ligt.m', 'r') 
			result_list.append((data_file, f.read()))		
	print result_list 
	os.chdir(cwd)
	for result in result_list:
		plot_result(result[0], result[1])
	
if __name__ == "__main__":
	main()
