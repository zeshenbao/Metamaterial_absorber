import cadquery as cq
from cadquery import exporters
from math import *


tile_wid = 1
tile_len = 1
tile_height = 2

def dog_side():
    foundation_thickness = 4
    h = tile_height/2
    angle = (pi/6)/2
    w = h*tan(angle)
    print(w)
    pts = [(0,0),
           (1.5*w, -1.5*h),

           (0.5*w, -2*h),
           (-1.5*w, -2*h),
           (-0.5*w, -1.5*h),
           (-w, -h)]

    geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-tile_wid)

    geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,-tile_wid/2,tile_height))

    dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(tile_len, tile_wid).extrude(-foundation_thickness))


    return dog_side


def make_sub():
        """Make the element to remove from union before adding with intersection """
        pts = [(tile_len/2, -tile_wid/2),
               (tile_len/2, tile_wid/2),
               (-tile_len/2, tile_wid/2)
            ]
        
        sub = cq.Workplane("XY").polyline(pts).close().extrude(tile_height)#.faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #skapas vid masspunkt
        
        return sub




ver = dog_side()#.center(0,0).circle(0.5).extrude(-6)
hor = dog_side().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))


inter = ver.intersect(hor)
union = ver.add(hor)
sub = make_sub()
diff = union.cut(sub)
corner = diff.add(inter)


exporters.export(ver, "ver.stl")
exporters.export(hor, "hor.stl")
#exporters.export(inter, "inter.stl")
#exporters.export(union, "union.stl")
#exporters.export(sub, "sub.stl")
#exporters.export(diff, "diff.stl")
#exporters.export(corner, "corner.stl")

#make dog leg in the middle extrude out to  
#cut ver and hor side parts and add them to intersect



