#!/usr/bin/env python
from celery import Celery
import os

from generate_data import run_script
from generate_data import airfoil
from convert2xml import convert_files_at_path as convert
from plot_result import plot_result

app = Celery('tasks', backend='amqp', broker='amqp://antus:antusantus@130.238.29.29/vhost_antus')


@app.task(bind=True)
def work(self, run_args, airfoil_args):
	# go to right place 
	os.chdir("../naca_airfoil")
	
	run_script(run_args["angle_start"], run_args["angle_stop"], run_args["n_angles"], run_args["n_nodes"], run_args["n_levels"])
	convert("msh/")
	
	path = "../msh/"
	os.chdir("navier_stokes_solver/")
	
	result_list = []
	
	for data_file in os.listdir(path):
		file_path, extension = os.path.splitext(data_file)
		if extension == ".xml":
			## start new worker
			airfoil(airfoil_args["num_samples"], airfoil_args["visc"], airfoil_args["speed"], airfoil_args["T"], path+data_file)
			f = open('results/drag_ligt.m', 'r')
			result_list.append((data_file, f.read()))

	return result_list
