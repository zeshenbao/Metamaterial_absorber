import cadquery as cq
from cadquery import exporters

thickness = 2
base_thickness = 3
height = 5

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
intersection = intersection_a.findSolid().intersect(intersection_b.findSolid())
#print(type(intersection)) #######################################################################
union_a = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(-thickness / 2)
)
union_b = (
    cq.Workplane("XZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(-thickness / 2)
)
corner = cq.CQ(union_a.union(union_b).union(intersection).findSolid())

# Displays the result of this script
#show_object(intersection)





exporters.export(intersection, "intersection.stl")