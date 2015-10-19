#!flask/bin/python

import os
import json
import time
import sys
import time
import shutil
from celery import Celery
from collections import Counter
import urllib2
import subprocess

app = Celery('proj', backend='amqp', broker='amqp://mava:orkarinte@130.238.29.120:5672/app2')

@app.task
def convertFile(fileName, mshFile):
	print "Started to process file: " + str(fileName)
	##########################################
	##### Conver file from *msh to *.xml #####
	##########################################
	newFile = open(fileName, "w")
	newFile.write(mshFile)
	newFile = open(fileName, "r")
	newFile.close()
	fileNameWithoutExtension = os.path.splitext(fileName)[0]
	xmlFileName = fileNameWithoutExtension + ".xml"
	print fileNameWithoutExtension
	subprocess.call(["dolfin-convert", fileName, xmlFileName])
	##########################################
	########## Copy airfoil to dir ###########
	##########################################
	subprocess.call(["mkdir", fileNameWithoutExtension])
	subprocess.call(["cp", "-a", "airfoil", fileNameWithoutExtension])

	##########################################
	########## Run airfoil on file ###########
	##########################################
	num = str(10)
	visc = str(0.0001)
	speed = str(10.)
	T = str(1)
	subprocess.call(["./airfoil", num, visc, speed, T, "../" + xmlFileName + " > output.log"], cwd=fileNameWithoutExtension+"/")
	##########################################
	######### Get drag_ligt.m values #########
	##########################################
	resultLists = readFile("/home/ubuntu/naca_airfoil/" +fileNameWithoutExtension+"/results/drag_ligt.m")
	os.system("rm -rf " + fileNameWithoutExtension + "*")
	return (fileName, resultLists)

@app.task
def readFile(fileName):
	theFile = open(fileName, "r").read()
	timeColumn = []
	liftColumn = []
	dragColumn = []
	lines = open(fileName, "r").readlines()
	for x in range(1, len(lines)):
		time = lines[x].strip().split()[0]
		timeColumn.append(time)
		lift = lines[x].strip().split()[1]
		liftColumn.append(lift)
		drag = lines[x].strip().split()[2]
		dragColumn.append(drag)
	resultList = []
	resultList.append(timeColumn)
	resultList.append(liftColumn)
	resultList.append(dragColumn)
	return resultList








