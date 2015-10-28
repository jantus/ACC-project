#!flask/bin/python
from flask import Flask, jsonify, request, render_template, url_for
from tasks import work as task
from plot_result import plot_result
import worker.server as worker
import time
import sys
import os


result_list = []

app = Flask(__name__, template_folder="/home/ubuntu/ACC-project/src")
@app.route('/')
def form():
	return render_template('site/form_submit.html')

@app.route('/runsh/', methods=['POST'])
def runsh():
	run_args = {}
	
	angle_start = request.form['angle_start']
	angle_stop = request.form['angle_stop']
	n_angles = request.form['n_angles']
	n_nodes = request.form['n_nodes']
	n_levels = request.form['n_levels']

	num_samples = request.form['num_samples']
	visc = request.form['visc']
	speed = request.form['speed']
	T = request.form['T'] 

	print angle_start
	print angle_stop
	print n_angles
	print n_nodes
	print n_levels
		
	print num_samples
	print visc
	print speed
	print T
	##########################################################	
	# Add workers	
	##########################################################	
	num_workers = int(n_angles)
	worker_name = "group15-worker-"

	for i in range(0, num_workers):
		print "Starting worker named: ", worker_name+str(i)
#		worker.terminate(worker_name+str(i))
#		worker.initialize(worker_name+str(i))
		
		print "Crated "+str(num_workers)+" workers"

#	time.sleep(20)

	
	#############################################################
	#	Create args
	#############################################################
	# run.sh script arguments
	run_args = {}
	run_args["angle_start"] = str(0)
	run_args["angle_stop"] = str(30)
	run_args["n_angles"] = str(1)
	run_args["n_nodes"] = str(200)
	run_args["n_levels"] = str(3)

	# airfoil script argumentes
	airfoil_args = {}
	airfoil_args["num_samples"] = str(num_samples)
	airfoil_args["visc"] = str(visc)
	airfoil_args["speed"] = str(speed)
	airfoil_args["T"] = str(T)

	angle_size = int(angle_stop) - int(angle_start) 
	angle_step = int(angle_size)/int(n_angles)
	a_list = [angle_step*i for i in range(0, int(n_angles)+1)]
	args_list = [] 
	for j in range(0, int(n_levels)+1):
		for i in a_list:
			filename = "r"+str(j)+"a"+str(i)+"n"+str(n_nodes)
			run_args = {}
			run_args["angle_start"] = str(angle_start)
			run_args["angle_stop"] = str(angle_stop)
			run_args["n_angles"] = str(n_angles)
			run_args["n_nodes"] = str(n_nodes)
			run_args["n_levels"] = str(n_levels)
			
			args = (filename, run_args, airfoil_args)
			args_list.append(args)

	display_list = []
	for elem in args_list:
		plot = elem[0]+str(elem[2])+".png"
		if os.path.isfile("static/"+plot):
			print "exists", plot
			global result_list
			result_list.append((plot, elem[0], elem[2]))
			
			display_list.append(plot)
		else:
			result = task.delay(elem[1], elem[2], elem[0])
			global result_list
			result_list.append((result, elem[0], elem[2]))

			display_list.append("Waiting for "+plot) 
	print result_list
	
	return render_template('site/results.html', result=display_list)

@app.route('/results/')
def results():
	display_list = []
	i = 0
	print result_list
	for result, filename, args in result_list:
		print result
		if type(result) is str:
			display_list.append(result) 
		else:
			print "not in if",result.ready() == True

			if result.ready() == True:
				print "in if",result.ready() == True
			
				res = result.get() 
				plot_result(res[0], res[1], args) 
				global result_list
				result_list[i] = (filename+".png", filename, args) 
			else: 
				display_list.append("Waiting for "+filename) 					
		i = i+1
			
	
	return render_template('site/results.html', result=display_list)


def old():
		
	# run.sh script arguments
	run_args = {}
	run_args["angle_start"] = str(0)
	run_args["angle_stop"] = str(30)
	run_args["n_angles"] = str(1)
	run_args["n_nodes"] = str(200)
	run_args["n_levels"] = str(3)

	# airfoil script argumentes

	airfoil_args = {}
	airfoil_args["num_samples"] = str(10)
	airfoil_args["visc"] = str(0.0001)
	airfoil_args["speed"] = str(10)
	airfoil_args["T"] = str(1)

	print run_args
	print airfoil_args
	print

	##########################################################	
	# Add workers	
	##########################################################	
	num_workers = 1
	worker_name = "group15-worker-"

	for i in range(0, num_workers):
		print "Starting worker named: ", worker_name+str(i)
		worker.terminate(worker_name+str(i))
		worker.initialize(worker_name+str(i))
		
		print "Crated "+str(num_workers)+" workers"

	time.sleep(20)

	##########################################################	
	# Add task
	##########################################################	
	
	xml_filename = "r0a0n200.xml"	
	result = task.delay(run_args, airfoil_args, xml_filename)
	print "Added Task"

	
	
	result_list = result.get()
	print "Got the result"
	print result_list
	
	
	print "creating plots"
	for result in result_list:
		plot_result(result[0], result[1])

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )	
