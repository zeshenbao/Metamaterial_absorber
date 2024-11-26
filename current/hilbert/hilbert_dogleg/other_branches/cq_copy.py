import cadquery as cq
from cadquery import exporters
from math import *


box = cq.Workplane("XY").box(1,1,2)
box2 = cq.Workplane("XY").box(1,2,0.5)


exporters.export(box, "box.stl")
exporters.export(box2, "box2.stl")
