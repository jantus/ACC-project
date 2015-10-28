from celery import Celery
from dolfin_convert import gmsh2xml
import os
import sys
import subprocess

NACA1='0'
NACA2='0'
NACA3='1'
NACA4='2'

os.putenv("LC_ALL", "en_US.UTF-8")
#CELERY_REDIRECT_STDOUTS = False
#app = Celery('airfoilWorker',backend='amqp',broke='amqp://')
app = Celery('airfoilWorker',backend='amqp',broker='amqp://asd:asd@130.238.29.166:5672/asd')
mshPath = "naca_airfoil/msh/"
currentDir = '/home/ubuntu/project/ACC-project'

def createResFolder(resPath):
    if os.path.isdir(currentDir+'/'+ resPath+'/results'):
        for file in os.listdir(resPath+'/results'):
            os.remove(resPath+'/results/'+file)
        for file in os.listdir(resPath+'/msh'):
            os.remove(resPath+'/results/'+file)
        for file in os.listdir(resPath+'/geo'):
            os.remove(resPath+'/results/'+file)
        os.rmdir(resPath + '/results')   
        os.rmdir(resPath + '/geo')
        os.rmdir(resPath + '/msh')    
        os.rmdir(resPath)
    os.makedirs(resPath)
    os.chdir(currentDir+ '/' + resPath)
    os.makedirs('geo')
    os.makedirs('msh')

def createMesh(angle,n_angles,n_nodes,n_level):
    geofile = 'a' + angle + 'n' + n_nodes + '.geo'
    mshFile = 'r0'+'a'+angle+'n'+n_nodes+'.msh'
    mshDir = currentDir+'/'+ resPath  + '/msh/'
    nacamsh = './home/ubuntu/project/ACC-project/naca_airfoil/naca2gmsh_geo.py'
    GMSHBIN = './usr/bin/gmsh'
    subprocess.call([nacamsh,NACA1,NACA2,NACA3,NACA4,str(angle),str(n_nodes),'>' + os.getcwd() + '/geo/'+geoFile])
    subprocess.call([GMSHBIN,'-v','0','-nopopup','-2','-o',currentDir+'/'+resPath+'/'+'msh/'+mshFile,currentDir+'/'+resPath+'geo'+'/'+geofile])
    outfile = ''
    for i in range(1,n_level):
        newname = 'r'+str(i)+'a'+angle+'n'+n_nodes+'.msh'
        mshFile = newname
        os.rename(mshFile,newname)
        subprocess.call([GMSHBIN,'-refine','-v','0', currentDir+'/'+resPath+'msh/'+newname])        
    file_path, file_extension = os.path.splitext(newname)
    outfile = 'r'+str(i)+'a'+angle+'n'+n_nodes+'.xml'
    msh2xml(mshDir+mshFile, file_path+'.xml')
    return  outfile

@app.task
def runairfoil(resPath,nSamples,nu,v,t,filename,angle,n_angles,n_nodes,n_level):
    create_respath(resPath)
    outfile = create_mesh(angle,n_angles,n_nodes,n_level)
    out_file = currentDir+'/msh/'+outfile
    airfoilpath =  './../naca_airfoil/navier_stokes_solver/airfoil'
    subprocess.call([airfoilpath,nSamples,nu,v,t,out_file],stdout=open(os.devnull,'w'))
    os.remove(out_file)
    return




