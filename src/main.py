from tasks import work as task
from plot_result import plot_result
import worker.server as worker
import time

def main():
		
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

	print "arguments are set"
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
	main()
