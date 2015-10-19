from flask import Flask
from flask import send_file
from generate_data import run_script
from airfoilWorker import runairfoil
import json
import os
from convert2xml import convert_files_at_path
fapp = Flask(__name__)

@fapp.route('/gen_meshes',methods=['get'])
def gen_meshes():
    angle_start = str(0)
    angle_stop = str(30)
    n_angles = str(10)
    n_nodes = str(200)
    n_levels = str(3)
    run_script(angle_start,angle_stop,n_angles,n_nodes,n_levels)
    return json.dumps({"gen":"finished"})

@fapp.route('/run_airfoil',methods=['get'])
def run_airfoil():
    taskList = []
    n = 0
    fileList = []
    
    for file in os.listdir('naca_airfoil/msh'):
    fileList.append(file)    
    for file in fileList():
        if(n > 2):
            break
        taskList.append(runairfoil.delay('res'+str(n),'10','0.0001','10','1',str(file)))
        n = n + 1
    for i in range(0,len(taskList)):
        while taskList[i].ready():
            continue
    return json.dumps({"airfoil":"finished"})

@fapp.route('/run',methods=['get'])
def run():
    obj = gen_meshes()
    obj2 = run_airfoil()
    return obj2

if __name__ == '__main__':
	fapp.run(host='0.0.0.0',debug=True)
            
    