import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO


#parameters
thickness=10.0
base_thickness=3.0
height=12.0

#noumber of pyramides
a=6
b=6

#code for intersection from Hilbert curve by M. Pettrof. In my case intersection is renamed to pyramide

intersection_a = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2, both=True)
)

print("intersection_a", type(intersection_a))

intersection_b = (
    cq.Workplane("XZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2, both=True)
)

print("intersection_b", type(intersection_b))

pyramide = intersection_a.findSolid().intersect(intersection_b.findSolid())

print("pyramide", type(pyramide))

block = cq.CQ(pyramide)

print("block", type(block))

#starting block
result=block

"""
#adding aditional pyramides
for i in range(a):
    for j in range(b):
        block= cq.CQ(pyramide) #Makes nev block every time, so there is no copy from before. Probably there is a better option, but for now it works
        moved_block=block.translate((i*(thickness), j*(thickness)))
        result=result.add(moved_block)

#Merging all shapes together
result.union(result)

#exporting
exporters.export(result, 'pyramide_absorber.step')
"""
