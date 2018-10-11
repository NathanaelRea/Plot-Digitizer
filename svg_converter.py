#!/usr/bin/env python

# svg_converter.py <svgfile> <xmin> <xmax> <ymin> <ymax>
#
# Convert an SVG path and rectangle to a tab-separated list of data
# points.
#
# The reference coordinates given in the arguments correspond to the
# corners of the rectangle in the SVG file. The SVG file must contain
# exactly one path and one rectangle (you can leave the reference
# raster).
#
# Copyright (c) OldOxygen (https://github.com/OldOxygen),
# Michael Danilov (https://github.com/OldOxygen), 2018
#
#
# BUGS
#
# * The path handling is extremely flaky and garbages when snaps are used.
#   Should we use proper SVG library?


import sys

def main(file, real_o_x, real_xmax, real_o_y, real_ymax):

	# svg file to convert
	svg = read_file(file)
	# sometimes <path is in defs, just want to skip them
	svg = svg.replace(find_between(svg,"<defs","</defs>"),"")

	# rectangle
	# find svg delta_x and delta_y, and xy of origin
	raw_rectangles = svg.split("<rect\n")
	svg_delta_x = float(find_between(raw_rectangles[1],"width=\"","\""))
	svg_delta_y = float(find_between(raw_rectangles[1],"height=\"","\""))
	svg_o_x = float(find_between(raw_rectangles[1],"x=\"","\""))
	svg_o_y = float(find_between(raw_rectangles[1],"y=\"","\"")) + svg_delta_y

	# create scale
	real_delta_x = real_xmax - real_o_x;
	real_delta_y = real_ymax - real_o_y;
	x_scale = real_delta_x / svg_delta_x
	y_scale = real_delta_y / svg_delta_y

	# lines
	raw_lines = svg.split("<path\n")
	del raw_lines[0]
	for line in raw_lines:
		past = [-svg_o_x, -svg_o_y]
		coords = find_between(line,"d=\"","\"")
		coords = coords.replace("m ","").replace("c ","").replace(" z","").split(" ")
		for coord in coords:
			tmp = list(map(float, coord.split(",")))
			tmp[0] += past[0]
			tmp[1] += past[1]
			past = list(tmp)
			tmp[0] *= x_scale
			tmp[1] *= y_scale
			print("{}\t{}".format(tmp[0] + real_o_x, - tmp[1] + real_o_y))


def read_file(filename):
	# Simple file read
	try:
		file_ = open(filename)
		txt = file_.read()
		file_.close()
		return txt
	except:
		input("Cannot find file: {}".format(filename))

def find_between(s, first, last):
	# Find substring between two subs in a str (s)
	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

if __name__ == "__main__":
       main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
