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






