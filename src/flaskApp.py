#!flask/bin/python

from flask import Flask, jsonify, request, render_template, url_for
from celery import group
import sys
import os
import time
import subprocess

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
	
	print 1, "- - - - - - - - Run start - - - - - - - -"
	########################
	##### Create *.msh #####
	########################
	time_1 = time.time()
	#subprocess.call(["./run.sh", angle_start, angle_stop, n_angles, n_nodes, n_levels])
	time_2 = time.time()
	print 2, time_2 - time_1
	#############################################
	##### Convert *.msh to *.xml + lite mer #####
	#############################################
	#appLocation = app.root_path
	#fileLocation = appLocation + "/msh/"
	#content = sorted(os.listdir(fileLocation))
	#response = group(convertFile.s(fileName, open(fileLocation+fileName, "r").read()) for fileName in content)
	#result = response.apply_async()
	#result.get()
	#time_3 = time.time()
	#print 3, time_3 - time_2
	#for t in result.get():
#		(fileNamePlot, data) = t
#		plot_file(fileNamePlot, data)
#	os.system("rm -rf  msh/*")
#	os.system("rm -rf  geo/*")

#	return render_template('site/runsh.html', 
#							angle_start=angle_start, 
#							angle_stop=angle_stop, 
#							n_angles=n_angles, 
#							n_nodes=n_nodes, 
#							n_levels=n_levels)


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )
