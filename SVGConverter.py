#!/usr/bin/python3
"""
For help with arguments:
SVGConverter.py -h

Convert an SVG path and rectangle to csv type output of notes

The reference coordinates given in the arguments correspond to the corners of
the rectangle in the SVG file. The SVG can contain any number of paths, and
will base the scale off the first rectangle in the file
It will output a csv for each path, separated by newline

Contributors
OldOxygen         (https://github.com/OldOxygen)
Michael Danilov   (https://github.com/mike402)
"""

import os
from xml.dom import minidom
from svg.path import parse_path
from argparse import ArgumentParser

def svg_to_csv(filename, delimiter, num_div, r_x_delta, r_y_delta, r_o_x, r_o_y):
    """Convert an svg file to a csv of scaled data points"""
    paths = svg_path_parse(filename)
    # grab scalers from file to shrink/expand csv values
    [svg_x, svg_y, x_scale, y_scale] = svg_scale(filename, r_x_delta, r_y_delta)
    # create a list of 
    out = []
    for curve in paths:
        for i in range(num_div):
            # svg path object is in complex form (like x + i*y)
            cur_complex = curve.point(i/num_div)
            # svg files have their own coordinate systems,
            # so we need to re-scale, then translate to the given origin
            x = (cur_complex.real - svg_x)*x_scale + r_o_x
            y = r_y_delta - (cur_complex.imag - svg_y)*y_scale + r_o_y
            out.append("{}{}{}".format(x, delimiter, y))
        out.append('')
    return out

def svg_path_parse(filename):
    """
    grabs all paths in svg with attribute 'd' (curves)
    then parses with svg.path into bezier objects, followed from:
    https://stackoverflow.com/questions/15857818/python-svg-parser#15857847
    icktoofay
    """
    doc = minidom.parse(filename) # could also use parseString?
    path_elements = doc.getElementsByTagName('path')
    path_strings = [path.getAttribute('d') for path in path_elements]
    doc.unlink()
    # parse each element in path_strings into svg objects
    for i,p in enumerate(path_strings):
        path_strings[i] = parse_path(p)
    return path_strings

def svg_scale(filename, r_x_delta, r_y_delta):
    """
    Find the scale factors in an svg file from a rectangle inside the file
    and the user input values of how big that rectangle should actually be
    """
    doc = minidom.parse(filename)
    # find the first rectangle element for scale
    rect = doc.getElementsByTagName('rect')[0]
    x = float(rect.getAttribute('x'))
    y = float(rect.getAttribute('y'))
    delta_x = float(rect.getAttribute('width'))
    delta_y = float(rect.getAttribute('height'))
    doc.unlink()
    # create scalers
    x_scale = r_x_delta / delta_x
    y_scale = r_y_delta / delta_y
    return [x, y, x_scale, y_scale]

def ui_selection(header, options, fltr=""):
    """Fairly simple ui for inputs"""
    options = [i for i in options if fltr in i.lower()]
    l = len(options)
    choices = list(map(str, range(1,l+1)))
    if l == 0: # quit if no files
        print(header)
        Exit("There are no files found with '{}'".format(
            fltr))
    elif l == 1: # return if only one option
        print(header)
        print("There was only one option '{}'".format(options[0]))
        print("\t(so I picked it for you)")
        return(options[0])
    while True:
        print(header)
        for i in range(l):
            print("\t{}: {}".format(choices[i],options[i]))
        choice = input()
        if choice in choices:
            return options[choices.index(choice)]
        call('clear' if os.name =='posix' else 'cls') 
        print("'{}' is not in the option list".format(choice))

def write_file(filename, data):
    """Simple file write, Converts to string if data object is not already"""
    if (type(data) == list) or (type(data) == tuple):
        data = '\n'.join(map(str,data))
    with open(filename, 'w') as f:
        f.write(data)
        
def Exit(exit_str):
    """Exit with a message"""
    print(exit_str)
    input("Press enter to exit")
    raise SystemExit

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="SVG FILE to read", metavar="FILE")
    parser.add_argument("-o", "--output", dest="output_file", default=None,
                        help="output FILE to write to, default=stdout", metavar="FILE")
    parser.add_argument("-n", dest="n", default=None, type=int,
                        help="number of points along path to output")
    parser.add_argument("-dx", "--deltax", dest="dx", default=None, type=float,
                        help="real x change in plot")
    parser.add_argument("-dy", "--deltay", dest="dy", default=None, type=float,
                        help="real y change in plot")
    parser.add_argument("-xo", "--xorigin", dest="xo", default=0, type=float,
                        help="x value start of origin")
    parser.add_argument("-yo", "--yorigin", dest="yo", default=0, type=float,
                        help="y vlaue start of origin")
    parser.add_argument("-d", "--delimiter", dest="d", default=',',type=str,
                        help="delimiter between xy output")
    args = parser.parse_args()
    if args.filename == None:
        files = os.listdir()
        args.filename = ui_selection("SVG file to parse:", files, ".svg")
    if args.dx == None:
        args.dx = float(input("Real X change of plot: "))
    if args.dy == None:
        args.dy = float(input("Real Y change of plot: "))
    if args.n == None:
        args.n = int(input("Number of Data Points: "))
    # bash interperets \t as t and \n as n
    # I don't think there's a way around hardcoding these
    if args.d == 't':
        args.d = '\t'
    elif args.d == 'n':
        args.d = '\n'
    # run to get csv values
    csv = svg_to_csv(args.filename, args.d, args.n, 
                     args.dx, args.dy, args.xo, args.yo)
    # write to file or stdout
    if args.output_file == None:
        print('\n'.join(map(str,csv)))
    else:
        write_file(args.output_file, csv)
