#!/usr/bin/python3

# svg_converter.py <svgfile> <xmin> <xmax> <ymin> <ymax>
#
# Convert an SVG path and rectangle to csv type output of notes
#
# The reference coordinates given in the arguments correspond to the corners of
# the rectangle in the SVG file. The SVG can contain any number of paths, and
# will base the scale off the first rectangle in the file
# It will output a csv for each csv, separated by newline
#
# Contributors
# OldOxygen         (https://github.com/OldOxygen),
# Michael Danilov   (https://github.com/mike402)

#import sys
from xml.dom import minidom
from svg.path import parse_path
from argparse import ArgumentParser


def svg_converter(filename, real_o_x, real_xmax, real_o_y, real_ymax):
    paths = svg_path_parse(filename)
    
    # rectangle
    # find svg delta_x and delta_y, and xy of origin
    [svg_o_x, svg_o_y, svg_delta_x, svg_delta_y] = svg_scale(filename)

    # create scale
    real_delta_x = real_xmax - real_o_x;
    real_delta_y = real_ymax - real_o_y;
    x_scale = real_delta_x / svg_delta_x
    y_scale = real_delta_y / svg_delta_y

    out = []
    num_div = input("How many divisions do you want per segment: ")
    for curve in paths:
        for i in range(1,num_div):
            cur_complex = curve.point(1/i)
            out.append("{},{}\n".format(cur_complex.real,cur_complex.imag))
    
    write_file(out_file, out)

# grabs all paths in svg with attribute 'd'
# then parses with svg.path
def svg_path_parse(filename):
    # https://stackoverflow.com/questions/15857818/python-svg-parser#15857847
    # icktoofay
    doc = minidom.parse(svg_file)  # parseString also exists
    path_strs = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()
    
    for i,p in enumerate(path_strings):
        path_strings[i] = parse_path(p)
    
    return path_strings


def svg_scale(filename):
    doc = minidom.parse(svg_file)
    #get first rectangle element
    rect = doc.getElementsByTagName('path')[0]
    x = float(rect.getAttribute('x'))
    y = float(rect.getAttribute('y'))
    delta_x = float(rect.getAttribute('width'))
    delta_y = float(rect.getAttribute('height'))
    doc.unlink()
    return [x, y, delta_x, delta_y]


#def ui_selection():
#    pass

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", type="str"
                        help="read SVG FILE", metavar="FILE")
    parser.add_argument("-o", "--output", dest="output_file", nargs = '?', const="stdout",
                        help="output FILE", metavar="FILE")
    #parser.add_argument("-q", "--quiet",
    #                    action="store_false", dest="verbose", default=True,
    #                    help="don't print status messages to stdout")

    args = parser.parse_args()
    
    print(args)
    input()
    
    if filename == None:
        files = os.listdir()
        filename = ui_selection("Pick an svg file to parse:", files, "svg")
    
    svg_converter(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
