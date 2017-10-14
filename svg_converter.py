import os
import time

def main():
	# This script converts svg bezier paths into a csv of x-y coordinates
	# Circles inside the svg will tell what to scale the coords by, and origin
	
	files = os.listdir()
	file = ui_selection("Pick an svg file to convert:", files, ".svg")
	svg = read_file(file)
	#sometimes <path is in defs, just want to skip them
	svg = svg.replace(find_between(svg,"<defs","</defs>"),"")

	# circles
	c = []
	raw_circles = svg.split("<circle\n")
	del raw_circles[0]
	for circle in raw_circles:
		x = float(find_between(circle,"cx=\"","\""))
		y = float(find_between(circle,"cy=\"","\""))
		c.append([x,y])
	
	# find svg delta_x and delta_y, and xy of origin
	max_x = max([i[0] for i in c])
	max_y = min([i[1] for i in c])
	for i in c:
		if not (i[0] == max_x or i[1] == max_y):
			origin = i
	o_x = origin[0]
	o_y = origin[1]
	svg_delta_x = max_x - o_x
	svg_delta_y = max_y - o_y
	
	# create scale
	real_delta_x = float(input("What is the real distance between circles (x dir)\n"))
	real_delta_y = float(input("What is the real distance between circles (y dir)\n"))
	x_scale = real_delta_x/svg_delta_x
	y_scale = real_delta_y/svg_delta_y
	
	# lines
	xy = []
	raw_lines = svg.split("<path\n")
	del raw_lines[0]
	for line in raw_lines:
		past = [-o_x, -o_y]
		coords = find_between(line,"d=\"","\"")
		coords = coords.replace("m ","").replace("c ","").replace(" z","").split(" ")
		for coord in coords:
			tmp = list(map(float, coord.split(",")))
			tmp[0] += past[0]
			tmp[1] += past[1]
			past = list(tmp)
			tmp[0] *= x_scale
			tmp[1] *= y_scale
			xy.append(tmp)
	
	#  add ',' delim, write csv
	out = ["{},{}".format(i[0],i[1]) for i in xy]
	out = "xcord,ycord\n" + "\n".join(out)
	
	filename = input("Filename to save data:\n")
	
	write_file(filename, out)
	
	Exit("###   Sucess   ###", 1)





def ui_selection(header,options,filter=""):
	# Simple cmd selector
	# Optional filter by string, I use it mainly for filetype
	options = [x for x in options if filter in x]
	l = len(options)
	choices = list(map(str, range(1,l+1)))
	while True:
		print(header)
		for i in range(l):
			print("\t{}: {}".format(choices[i],options[i]))
		choice = input()
		if choice in choices:
			return options[choices.index(choice)]
		os.system("cls")
		print("'{}' is not in the option list".format(choice))

def read_file(filename):
	# Simple file read
	try:
		file_ = open(filename)
		txt = file_.read()
		file_.close()
		return txt
	except:
		input("Cannot find file: {}".format(filename))

def write_file(filename, data):
	# Simple file write
	file_ = open(filename, 'w')
	file_.write(data)
	file_.close()

def find_between(s, first, last):
	# Find substring between two subs in a str (s)
	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

def p(var):
	# Simple tool for quickly debugging vars
	print(var)
	input("Pause.")

def Exit(exit_str, n):
	# Sleep to be able to read exit message
	os.system('cls')
	print(exit_str)
	time.sleep(n)
	raise SystemExit

if __name__ == "__main__":
	main()