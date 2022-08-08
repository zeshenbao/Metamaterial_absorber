import cadquery as cq
from cadquery import exporters
from math import *


pts = [(-0.5, 0),
       (0.5, 0),
       (0.5, -0.5),
       (-0.5, -0.5)]

test = cq.Workplane("XZ").center(0,-0.5).polyline(pts).close().extrude(0.5).mirror(mirrorPlane="XZ", union = True)

cir = cq.Workplane("XY").center(0,0).circle(0.6).extrude(-1)

test.add(test.translate((0,1.2,0))).add(cir)#.add(test.translate((0,0,2)))
exporters.export(test, "test.stl")
