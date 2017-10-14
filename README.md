# Plot-Digitizer
Get very accurate plot data by using an svg file that was traced with bezier curves


This is just a basic tool to be able to convert an image into a plot.


* Insert the image into inkscape and draw bezier curves around it.
![Closeup](https://raw.githubusercontent.com/OldOxygen/Plot-Digitizer/master/docs/close.png)

Here is a completed example:

![Bezier Nodes](https://raw.githubusercontent.com/OldOxygen/Plot-Digitizer/master/docs/all_nodes.png)

*As you can see, it is made from two lines. This is okay, but the script will place the points right after one another in the csv, and so if they are not next to one another, there will be a line connecting them when plotted*

* Select all the nodes, and click the "add more in-between" button a few times until satisfied.
![More Nodes](https://raw.githubusercontent.com/OldOxygen/Plot-Digitizer/master/docs/more_nodes.png)

* Add three circles, one for origin, one for xmax, and one for ymax.
![Extents](https://raw.githubusercontent.com/OldOxygen/Plot-Digitizer/master/docs/extents.png)

* Save the file, and run the python script in the same directory as it.
It will prompt for the "real" distance between the circles for x and y directions. This will be the numbers on the actual plot/picture itself. In this example, they were 7" and 250lbs, without units.

The script makes a csv of the nodes that were on the bezier curve.

Here is the sample output. The left is a simple plot example in excel. The right is a bit more clean in R.

![Output](https://raw.githubusercontent.com/OldOxygen/Plot-Digitizer/master/docs/output.png)

*With black as test data from Oesterle et al (1979) B9 wall sample, and blue as model results (if you were curious)*

I would like it if adding nodes in-between was not needed, however I'm not sure how bezier curves work/ or are saved, and so I don't know how to implement it.

Since I'm new, if there are any changes that might help me get better feel free to correct me, and I'll try to learn form them and implement them.

Thanks!
