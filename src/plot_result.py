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
import matplotlib
# Force matplotlib to not use any Xwondows backend.
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os.path

###############################################################################
# Takes a .m file that is created by the airfoil binary and creates a plot 
# from the data. Must be in the same directory as the .m file
# Arguments:
#       filename: Path o the file
###############################################################################
def plot_file(filename):
        f = open("drag_ligt.m", "r")
        s = f.read().split('\n')
        plot_result(s)

def plot_result(filename, result_string):
    time = []
    drag = []
    lift = []
    data_list = result_string.split('\n')
    for line in data_list[1:]:
    	elements = line.split('\t')
        if len(elements) == 3: 
	       	time.append(float(elements[0]))
	        drag.append(float(elements[1]))
	        lift.append(float(elements[2]))

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

