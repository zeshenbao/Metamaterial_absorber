# Metamaterial_absorber



## 20/04-22
1. Setting up git repository and downloading necessary software and documents to prepare for the project.
* Added old_files folder to repo
* Installed Freecad and added Cadquery extension


## 21/04-22
* Set up the correct enviroment to run absorber codes with Cadquery2 with Conda
* Tested the step files with Freecad 0.19

## 13/06-22
Plan:
1. Try 3D-printing something
2. Start learning about cadquery methods 
3. Start to make basic geometries

Did: 
1. Printed a violin test model and learned to: 
* Send things to formlabs printer via preform. 
* Preparing the printer for printing and removing the print.
* Washing in isopropanol manually and with machine and also curing it.

2. Looked at different examples of basic geometries of different cadquery objects.
* Learned basic methods in cadquery.

3. Tried to make a basic pyramid.

Questions \& To do:
* Learn to refill the printer with liquid.
* Learn how to move and rotate in Cadquery workplane to start iterating. (Look into .add, .rotate, .union, .translate methods)

## 14/06-22

Plan:
1. Learn .translation, <del>.rotation</del>, .add methods
2. Make a 9x9 pyramid absorber
<del> 3. Make a dogleg absorber </del>
4. Try other patterns (Hilbert, translation + rotation)
* start with simple cross section, (rectangular --> triangular --> dogleg)
* start with small section --> larger hilbert curves

Did: 
1. Looked at many example codes and learned to use methods .add and .translation.
2. Printed out a 30x30 pyramid wall with 1 mm between pyramids. 

<img src="log_images/14_06_2022/IMG_4104.JPG" alt="wall" width="200"/>
Figure1. print of pyramid wall from the side.<br><br>


<img src="log_images/14_06_2022/IMG_4107.JPG" alt="wall" width="200"/>
Figure2. print of pyramid wall from above.<br><br>

3. Started to print 25 25x25 updated pyramid walls to check printer properties.



Questions:
* What is/ how to make different types: Workplane, solid
* Some parts of the prints gets deformed, also pyramid heads are not sharp in different regions. Some supports are missing and noise during print.
* We could make some test patterns and print those 3-5 times to see if deformation happen on same spot or different.

## 15/06-22

Plan:
1. Study the print.
2. Finish writing the geometry file, add dog_leg later.
3. Start making Hilbert curve with blocks, continue to pyramid which requires corner sections, etc.

Did:
1. We studies the print and looks like the print is very dependent on the film quality and condition. We should change to a new film for optimal prints. The metal plating seemed fine. 
<p float="left">
  <img src="log_images/15_06_2022/above.jpg"  width="200"/>
  <img src="log_images/15_06_2022/left.jpg"  width="200"/>
  <img src="log_images/15_06_2022/right.jpg"  width="200"/>
  <img src="log_images/15_06_2022/front.jpg"  width="200"/>
  <img src="log_images/15_06_2022/back.jpg"  width="200"/>
</p>

2. Finished the geometry class file.



