#!/usr/bin/python
###############################################################################
#
# Name: plot_file
# Arguments (0):
# 	
# Output: 
# Example:
###############################################################################
import os
import matplotlib.pyplot as plt
import os.path

###############################################################################
# Takes a .m file that is created by the airfoil binary and creates a plot 
# from the data. Must be in the same directory as the .m file
# Arguments:
#	filename: Path o the file
###############################################################################
def plot_file(filename, data):
	f = open("drag_ligt.m", "r")
	s = f.read().split('\n')
	time = data[0]
	lift = data[1]
	drag = data[2]
	for line in s[1:]:
		l = line.split(' ')
		elemlist = []
		for element in l:
			if not element == "":
				elemlist.append(element)
		time.append(elemlist[0])
		drag.append(elemlist[1])
		lift.append(elemlist[2])

	plt.gca().set_color_cycle(['blue', 'red'])
	plt.plot(time, drag)
	plt.plot(time, lift)
	plt.grid(True)

	plt.legend(['Drag force', 'Lift force'])
	plt.xlabel('Time')
	plt.ylabel('Force')
	plt.title(filename)
	plt.yscale('log')
	plt.savefig(os.path.splitext(filename)[0] + '.png')

