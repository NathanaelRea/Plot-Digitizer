#!/usr/bin/python3

# For help with arguments:
# SVGConverter.py -h
#
# Convert an SVG path and rectangle to csv type output of notes
#
# The reference coordinates given in the arguments correspond to the corners of
# the rectangle in the SVG file. The SVG can contain any number of paths, and
# will base the scale off the first rectangle in the file
# It will output a csv for each path, separated by newline
#
# Contributors
# OldOxygen         (https://github.com/OldOxygen),
# Michael Danilov   (https://github.com/mike402)

import os
from xml.dom import minidom
from svg.path import parse_path
from argparse import ArgumentParser
    
def svg_to_csv(filename, dilimeter, num_div, r_x_delta, r_y_delta,
               r_o_x = 0, r_o_y = 0):
    paths = svg_path_parse(filename)

    [svg_x, svg_y, x_scale, y_scale] = svg_scale(filename, r_x_delta, r_y_delta)

    out = []
    for curve in paths:
        for i in range(num_div):
            cur_complex = curve.point(i/num_div)
            x = (cur_complex.real + r_o_x - svg_x) * x_scale
            # I actually don't know why this works for y, found by trial & error
            y = r_y_delta - (cur_complex.imag + r_o_y - svg_y) * y_scale
            out.append("{}{}{}".format(x,dilimeter,y))
        out.append('')
    return out

# grabs all paths in svg with attribute 'd'
# then parses with svg.path into bezier curve
def svg_path_parse(filename):
    # https://stackoverflow.com/questions/15857818/python-svg-parser#15857847
    # icktoofay
    doc = minidom.parse(filename)  # parseString also exists
    path_elements = doc.getElementsByTagName('path')
    path_strings = [path.getAttribute('d') for path in path_elements]
    doc.unlink()
    
    for i,p in enumerate(path_strings):
        path_strings[i] = parse_path(p)
    
    return path_strings

def svg_scale(filename, r_x_delta, r_y_delta):
    doc = minidom.parse(filename)
    #get first rectangle element
    rect = doc.getElementsByTagName('rect')[0]
    x = float(rect.getAttribute('x'))
    y = float(rect.getAttribute('y'))
    delta_x = float(rect.getAttribute('width'))
    delta_y = float(rect.getAttribute('height'))
    doc.unlink()

    # create scale
    x_scale = r_x_delta / delta_x
    y_scale = r_y_delta / delta_y
    
    return [x, y, x_scale, y_scale]

# Selection function
def ui_selection(header, options, fltr="", quick_select=""):
	# use options for filetype usually, just a quick filter
	options = [i for i in options if fltr in i.lower()]
	# optional quick_select to get a common file name
	if quick_select != "":
		options = [i for i in options if quick_select in i.lower()]
	l = len(options)
	choices = list(map(str, range(1,l+1)))
	if l == 0: # quit if no files
		print(header)
		# This will probably also trigger if quick_select not found
		Exit("There are no selections possible with '{}' or '{}'".format(
            fltr, quick_select) ,30)
	elif l == 1: # return if only one option
		print(header)
		print("There was only one option ({})".format(options[0]))
		print("\n\tso I picked it for you")
		return(options[0])
	while True:
		print(header)
		for i in range(l):
			print("\t{}: {}".format(choices[i],options[i]))
		choice = input()
		if choice in choices:
			return options[choices.index(choice)]
		os_dep("clear")
		print("'{}' is not in the option list".format(choice))

# Simple file write, also checks for list/tuple
def write_file(filename, data):
	if (type(data) == list) or (type(data) == tuple):
		data = j_l(data, "\n")
	# Need to write empty files, or things will break
	with open(filename, 'w') as f:
		f.write(data)

# join list into a string
def j_l(l, space=" ", round_dec=None):
	if round_dec == None:
		return space.join(map(str,l))
	else:
		l = [round(e,round_dec) for e in l]
		return space.join(map(str,l))
		
# Exit after specific time, with exit message
def Exit(exit_str, n):
	print(exit_str)
	time.sleep(n)
	raise SystemExit

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="read SVG FILE", metavar="FILE")
    parser.add_argument("-o", "--output", dest="output_file", default=None,
                        help="output FILE", metavar="FILE")
    parser.add_argument("-div", dest="div", default=None, type=int,
                        help="number of points along path to output")
    parser.add_argument("-dx", "--deltax", dest="dx", default=None, type=float,
                        help="actual x change in plot")
    parser.add_argument("-dy", "--deltay", dest="dy", default=None, type=float,
                        help="actual y change in plot")
    parser.add_argument("-xo", "--xorigin", dest="xo", default=0, type=float,
                        help="x value start of origin")
    parser.add_argument("-yo", "--yorigin", dest="yo", default=0, type=float,
                        help="y vlaue start of origin")
    parser.add_argument("-dil", "--dilimeter", dest="dil", default=',',type=str,
                        help="dilimeter of (x,y) output")
    args = parser.parse_args()

    if args.filename == None:
        files = os.listdir()
        args.filename = ui_selection("Pick an svg file to parse:",files,".svg")
    if args.dx == None:
        args.dx = float(input("Actual X change of plot: "))
    if args.dy == None:
        args.dy = float(input("Actual Y change of plot: "))
    if args.div == None:
        args.div = int(input("Number of Data Points: "))

    # bash interperests \t as t
    # just want easy user input for likely dilimeter chars
    if args.dil == 't':
        args.dil = '\t'
    elif args.dil == 'n':
        args.dil = '\n'

    out = svg_to_csv(args.filename, args.dil, args.div, 
                     args.dx, args.dy, args.xo, args.yo)
    
    if args.output_file == None:
        for line in out:
            print(line)
    else:
        write_file(args.output_file, out)
