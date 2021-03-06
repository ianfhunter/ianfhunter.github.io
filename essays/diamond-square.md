---
layout: essay
type: essay
title: Diamond-Square Terrain Generation
# All dates must be YYYY-MM-DD format!
date: 2018-12-09
labels:
  - Engineering
---

Here’s an interesting little algorithm I coded up before an interview – Terrain generation with the Diamond-Square Algorithm.

The algorithm itself is quite simple, but makes some nice graphs.

[diamond-square-algorithm](https://web.archive.org/web/20160420145841/https://en.wikipedia.org/wiki/Diamond-square_algorithm)

Initialize the corners of your N*N area randomly.
Square Section – Get the center point of your corners and set it to be the average of those 4 corners ± a random amount
Diamond Section – Get the center of each edge and set itto be the average of the surrounding diamond shape ± a random amount
In the example image, the left red point would be the average of the black points above, below and to the right of it – but you should include a fourth point if it exists.
Repeat until your grid is populated.

![3d Heatmap #3](https://ianfhunter.github.io/images/ds_algorithm.png) 


Here’s what this looks like with a simple heat map in 2D:

![2d Heatmap](https://ianfhunter.github.io/images/ds_heatmap-2d.png)

And in 3D:

![3d Heatmap #1](https://ianfhunter.github.io/images/ds_heatmap-3d.png)
<img src="https://ianfhunter.github.io/images/terrain-map-3d.png" alt="3D Heatmap #2" width="800"/>

This is a very simple algorithm to implement, but quite effective for what it does. You can change the random variant to increase the choppiness/smoothness of the resultant graph. The more points in the grid, the better this looks. Take this high-N example from playful.js for example:

![3d Heatmap #3](https://ianfhunter.github.io/images/ds_realism.png) 
 
Setting the sea level in your render is a matter of picking a Y-level and wherever there isn’t any rock below this point, fill the area with water. This is a pretty nice way to get both lakes and hills in one step.

There’s also an added benefit of exporting the co-ordinates so you only have to ever compute the terrain once.

You can browse the source of my implementation (In Python 2.7) on my [Github](https://web.archive.org/web/20160420145841/https://github.com/ianfhunter/DiamondSquare)
