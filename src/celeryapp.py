from celery import Celery
from generate_data import airfoil

celeryapp = Celery('tasks', backend='amp', broker='amqp://')

@celeryapp.task(bind=True)
def run_airfoil(data_file): 
	num_samples = str(10)
	visc = str(0.0001)
	speed = str(10)
	T = str(1)

	## run airfoul
	path = "../../msh/"
	filename, _ = os.path.splitext(data_file) 
	if not os.path.exists(filename):
		os.makedirs(filename) 
		os.chdir(filename)
		
		data_file = path+data_file
		## start new worker
		print "Start runnning airfoil on file", data_file
		airfoil(num_samples, visc, speed, T, data_file)

app = Celery('tasks', backend='amqp', broker='amqp://antus:antusantus@130.238.29.29/vhost_antus')



@app.task()
def work(run_args, airfoil_args)

	# Go to the right directory
	cwd = os.getcwd()
	os.chdir("../naca_airfoil") 
	
	# run script
	angle_start = run_args[0]
	angle_stop = run_args[1]
	n_angles = run_args[2]
	n_nodes = run_args[3]
	n_levels = run_args[4]

	run_script(angle_start, angle_stop, n_angles, n_nodes, n_levels)

	## convert files
	convert("msh/") 	

	num_samples = airfoil_args[0]
	visc = airfoil_args[1]
	speed = airfoil_args[2]
	T = airfoil_args[3]

	## run airfoul
	path = "../msh/"
	for data_file in os.listdir(path):
		print os.getcwd()
		file_path, extension = os.path.splitext(data_file) 
		if extension == ".xml":
			## start new worker
			print data_file
			airfoil(num_samples, visc, speed, T, path+data_file)

	
