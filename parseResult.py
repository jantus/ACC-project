


path = "results/"
filename = "drag_ligt.m"

f = open(path+filename, "r")
file_content = f.read()
content_list = file_content.split("\n")

sum_lift = 0
sum_drag = 0

for line in content_list[1:]:
	element = line.split("\t")
	if len(element) < 3:
		continue
	sum_lift += float(element[1])
	sum_drag += float(element[2])
	
print sum_drag, sum_lift
print "lift/drag: ", sum_lift/sum_drag
