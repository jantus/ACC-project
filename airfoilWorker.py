from celery import Celery
from dolfin_convert import gmsh2xml
import os
import sys
import subprocess

os.putenv("LC_ALL", "en_US.UTF-8")
#CELERY_REDIRECT_STDOUTS = False
app = Celery('airfoilWorker',backend='amqp',broke='amqp://')

mshPath = "naca_airfoil/msh/"

@app.task
def runairfoil(resPath,nSamples,nu,v,t,filename):
    out_file = ""
    file_path, file_extension = os.path.splitext(filename)
    if file_extension == ".msh":
        in_file = mshPath+filename
        out_file = mshPath+file_path+".xml"
        if not(os.path.isfile(out_file)):
            gmsh2xml(in_file, out_file)
        if os.path.isfile(in_file):
            try:
                os.remove(in_file)
            except : 
                print "Could not remove "+str(in_file)+" due to unexpected error:", sys.exc_info()[0]
    else:
        out_file = filename
    currentDir = os.getcwd()
    if os.path.isdir(resPath):
        for file in os.listdir(resPath+'/results'):
            os.remove(resPath+'/results/'+file)
        os.rmdir(resPath+'/results')
        os.rmdir(resPath)
    os.makedirs(resPath)
    os.chdir(currentDir+ '/' + resPath)
    airfoilpath =  './../naca_airfoil/navier_stokes_solver/airfoil'
    outPath = '../'+out_file    
    subprocess.call([airfoilpath,nSamples,nu,v,t,outPath],stdout=open(os.devnull,'w'))
    return




