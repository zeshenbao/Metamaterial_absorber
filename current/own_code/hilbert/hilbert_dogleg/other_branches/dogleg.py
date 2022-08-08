import cadquery as cq
from cadquery import exporters
from math import *

tile_height = 2
tile_wid = 1
tile_len = 1
foundation_thickness = 4
h = tile_height/2
angle = (pi/6)/2
w = h*tan(angle)
print(w)
pts = [(0,0),
       (1.5*w,-1.5*h),
       (0.5*w, -2*h),
       (-1.5*w, -2*h),
       (-0.5*w, -1.5*h),
       (-w, -h)]

geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-tile_wid)

geo_xy = cq.Workplane("XY").add(geo_xz).faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness)


exporters.export(geo_xy, "dogleg2.stl")
