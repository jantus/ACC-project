from flask import Flask
from generate_data import run_script
import json
from convert2xml import convert_files_at_path
fapp = Flask(__name__)

@fapp.route('/run',methods=['get'])
def run():
    angle_start = str(0)
    angle_stop = str(30)
    n_angles = str(10)
    n_nodes = str(200)
    n_levels = str(3)
    run_script(angle_start,angle_stop,n_angles,n_nodes,n_levels)
    #convert2xml('msh')
    return json.dumps({'message':'mesh generation done'}  

