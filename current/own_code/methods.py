


### Examples
# cq.Workplane("XY").box(3.0,2.0,0.5) #select workplane "XY" and make a box in the plane 
# cq.Workplane("front").rect(1, 1).workplane(offset=2.0).circle(0.001).loft(combine=True)



### Workplanes
# .Workplane("XY"): select workplane
# "front": == "XY"
# .workplane(offset=2.0): move 2.0 in the current direction
# .workplaneFromTagged("baseplane"): reselect workplane "baseplane"
# .tag("baseplane"): tag baseplane

### Directions
# .faces(">Z"): face in positive Z



### Geometries
# .rect: make rectangle
# .circle: make circle
# .box: make box




### Getting geometries and combinations
# .loft(combine="True"): loft two surfaces
# .extrude(thickness): cut out geometry in workplane direction
# .union: same as r = a+b, r = a.union(b), r = a|b (__or__ operator)
# .intersect: same as r = a&b
# .cut: same as r = a-b



### Questions
#how to offset in other directions?
# .add()
# .translate()
# .rotate()
# .union()


### Algoritm
# -- pyramid function
# start from baseplane and tag it
# make a pyramid -- 
# return to baseplane and ##how to offset in other directions?? #iterate with offset direction
# make the same pyramid --

