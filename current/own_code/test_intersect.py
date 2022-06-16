import cadquery as cq
from cadquery import exporters


box = cq.Workplane("XY").box(1,1,1).translate((0.5,0.5,0))
sph = cq.Workplane("XY").sphere(1)

result = box.intersect(sph)

exporters.export(result, "intersect.stl")
