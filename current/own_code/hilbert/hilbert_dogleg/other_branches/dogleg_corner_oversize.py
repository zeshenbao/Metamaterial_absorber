import cadquery as cq
from cadquery import exporters
from math import *

#cross_wid = 1.5
tile_wid = 1
tile_len = 1
tile_height = 3

def dog_side():
    global d
    
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

    d = 1.5*w-tile_len/2
    
    geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-(tile_wid+2*d)).translate((0, -d, 0)) #add twp stick out part and then shift with one shift out to get one shift out part every side.

    geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,-tile_wid/2,tile_height))

    dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(tile_len, tile_wid).extrude(-foundation_thickness))

    #circle = cq.Workplane("XZ").center(0.5*w+(tile_len/2-0.5*w)/2, 0).circle((tile_len/2-0.5*w)/2).extrude(tile_len*2+1).mirror(mirrorPlane="XZ", union=True)
    #circle = cq.Workplane("XZ").center(tile_len/2, 0).circle(0.1).extrude(tile_len).mirror(mirrorPlane="XZ", union=True)


    #dog_side = dog_side.cut(circle)


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


def make_intersect(ver, hor):
    inter = ver.intersect(hor)

    return inter


ver_half_left = dog_side().faces(">Y").workplane(-(0.5+d)).split(keepBottom=True)
ver_half_right = dog_side().faces(">Y").workplane(-(0.5+d)).split(keepTop=True)

hor_half_down = dog_side().rotate((0,0,0), (0,0,1), 90).faces(">X").workplane(-(0.5+d)).split(keepBottom=True)
hor_half_up = dog_side().rotate((0,0,0), (0,0,1), 90).faces(">X").workplane(-(0.5+d)).split(keepTop=True)


corner_left_down = make_intersect(ver, hor).add(ver_half_left).add(hor_half_down)
corner_left_up = make_intersect(ver, hor).add(ver_half_left).add(hor_half_up)
corner_right_down = make_intersect(ver, hor).add(ver_half_right).add(hor_half_down)
corner_right_up = make_intersect(ver, hor).add(ver_half_right).add(hor_half_up)

#print(ver)
#print(hor)
exporters.export(ver, "ver_dot.stl")
exporters.export(hor, "hor_dot.stl")
exporters.export(ver_half_left, "ver_half_dot.stl")
exporters.export(hor_half_down, "hor_half_dot.stl")
#exporters.export(hor, "hor.stl")
exporters.export(make_intersect(ver, hor), "inter_dot.stl")
#exporters.export(union, "union.stl")
#exporters.export(sub, "sub.stl")
#exporters.export(diff, "diff.stl")
#exporters.export(corner, "corner.stl")


exporters.export(corner_left_down, "corner_left_down_dot.stl")
exporters.export(corner_left_up, "corner_left_up_dot.stl")
exporters.export(corner_right_down, "corner_right_down_dot.stl")
exporters.export(corner_right_up, "corner_right_up_dot.stl")



#make dog leg in the middle extrude out to  
#cut ver and hor side parts and add them to intersect
#make a function to make thing if you want a deep copy


