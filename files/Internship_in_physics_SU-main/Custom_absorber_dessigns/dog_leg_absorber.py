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
n=6

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

pyramide = intersection_a.findSolid().intersect(intersection_b.findSolid())
block = cq.CQ(pyramide)

h=6.5
t=4.0
x=0.9
#v=h*t/(4*x)

base=1.5
L=60.0


pts = [
    (0.0,0.0),
    (t+x,0.0),
    (t+x,base),
    (t,base),
    (t+x,base+h/2),
    (t-2*x,base+2*h),
    (0.0, base+h),
    (x,base+h/2),
    (0, base)
]


polyline_block=cq.Workplane("front").polyline(pts).close().extrude(L)


#starting block
result=polyline_block

#adding aditional pyramides
for i in range(n):
    #block= cq.CQ(pyramide) #Makes nev block every time, so there is no copy from before. Probably there is a better option, but for now it works
    moved_block=polyline_block.translate((i*(t+x), 0))
    result=result.add(moved_block)
    result.union(result)

#Merging all shapes together
result.union(result)

#exporting
exporters.export(result, 'dog_leg_absorber.step')