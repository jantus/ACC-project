from celery import Celery
from dolfin_convert import gmsh2xml
import os
import sys
import subprocess

os.putenv("LC_ALL", "en_US.UTF-8")
#CELERY_REDIRECT_STDOUTS = False
#app = Celery('airfoilWorker',backend='amqp',broke='amqp://')
app = Celery('airfoilWorker',backend='amqp',broker='amqp://asd:asd@130.238.29.83:5672//asd')
mshPath = "naca_airfoil/msh/"
currentDir = ""
@app.task
def runairfoil(resPath,nSamples,nu,v,t,filename,mesh_contents):
    os.chdir('/home/ubuntu/project/ACC-project')
    currentDir = os.getcwd()
    out_file = ""
    file_path, file_extension = os.path.splitext(filename)
    if file_extension == ".msh":
        in_file = currentDir + '/' + mshPath+filename
        print in_file
        out_file = currentDir+'/'+mshPath+file_path+".xml"
        if not(os.path.isfile(out_file)):
            f = open(currentDir+'/'+mshPath+filename,'rw')
            f.write(mesh_contentes)
            f.close
            gmsh2xml(in_file, out_file)
        if os.path.isfile(in_file):
            try:
                os.remove(in_file)
            except : 
                print "Could not remove "+str(in_file)+" due to unexpected error:", sys.exc_info()[0]
    else:
        out_file = currentDir+'/'+filename
    if os.path.isdir(currentDir+'/'+resPath):
        if os.path.isdir(currentDir+'/'+ resPath+'/results'):
            for file in os.listdir(resPath+'/results'):
                os.remove(resPath+'/results/'+file)
            os.rmdir(resPath+'/results')
        os.rmdir(resPath)
    os.makedirs(resPath)
    os.chdir(currentDir+ '/' + resPath)
    airfoilpath =  './../naca_airfoil/navier_stokes_solver/airfoil'
    subprocess.call([airfoilpath,nSamples,nu,v,t,out_file],stdout=open(os.devnull,'w'))
    os.remove(out_file)
    return




