from cadquery import Vertex
import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO

from pyramid import pyramid
"""
base = pyramid((1,1),1)
pyr1 = base.translate((1,1,1))

#pyr2 = pyramid((1,1),1)
pyr2 = base.translate((2,2,2))
pyr3 = base.translate((3,3,3))

#print(type(pyr2))

result = pyr1.add(pyr2).add(pyr3)

exporters.export(result, "pyr_translate_test2.stl")
"""



"""
result = cq.Workplane("XY").tag("baseplane").rect(1,1).workplane(offset=1).circle(0.001).loft(combine=True)

result = result.workplaneFromTagged("baseplane").center(1,0).rect(1,1).workplane(offset=1).circle(0.001).loft(combine=True)


exporters.export(result, "pyra_method2.stl")
"""


"""
pyr1 = cq.Workplane("XY").rect(1,1).workplane(offset=1).circle(0.001).loft(combine=True)

pyr2 = cq.Workplane("XY").center(1,0).rect(1,1).workplane(offset=1).circle(0.001).loft(combine=True)

result = pyr1.add(pyr2)

exporters.export(result, "pyra_method3.stl")
"""
#base = (cq.Workplane("XY").rect(1,1).workplane(offset=1).circle(0.001).loft(combine=True))

base = (cq.Workplane("XY").rect(1,1).extrude(5).faces(">Z").rect(1,1).workplane(offset=2).circle(0.001).loft(combine=True)) #bättre att inte använda loft för snabbare kod

result = cq.Workplane("XY")
#result = base

length = 25
width = 25

for i in range(length):
    for j in range(width):
        pyr = base.translate((i,j,0))
        result.add(pyr)
    print(i)

#base_platform = cq.Workplane("XY").rect(length, width).extrude(-2).translate((length/2,width/2,0))

#result.add(base_platform)

exporters.export(result, "pyramid_wall_with_platform25.stl")
        
        
        
