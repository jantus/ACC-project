from celery import Celery
from dolfin_convert import gmsh2xml
import os
import sys
import subprocess

os.putenv("LC_ALL", "en_US.UTF-8")
CELERY_REDIRECT_STDOUTS = False
app = Celery('airfoilWorker',backend='amqp',broke='amqp://')

path = "../../msh/"

@app.task
def runairfoil(resPath,nSamples,nu,v,t,filename):
    os.makedirs(resPath
    os.chdir(resPath)
    out_file = ""
    file_path, file_extension = os.path.splitext(filename)
    if file_extension = ".msh":
        in_file = path+filename
        out_file = path+file_path+".xml"
        if os.path.isfile(out_file):
            continue
        else:
            gmsh2xml(in_file, out_file)
        if os.path.isfile(in_file):
            try:
                os.remove(in_file)
            except : 
                print "Could not remove "+str(in_file)+" due to unexpected error:", sys.exc_info()[0]
    else:
        out_file = filename
        subprocess.call(['./navier_stokes_solver/airfoil',nSamples,nu,v,t,out_file])
        
    return




