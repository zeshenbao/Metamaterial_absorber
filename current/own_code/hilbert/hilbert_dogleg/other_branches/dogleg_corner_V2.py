
import cadquery as cq
from cadquery import exporters
from math import *

scale = 10

#cross_wid = 1.5
tile_wid = 1 * scale
tile_len = 1 * scale
tile_height = 3 * scale

def dog_side():
    global d, w
    
    foundation_thickness = 4 * scale
    angle = (pi/6)/2
    
    h = tile_height/2
    w = h*tan(angle)
    
    #print(w)
    k = 1/tan(2*angle)
    k_w = 1/(1-tan(angle)**2) # koefficient front of w at lowest point
    a = tile_len - 2*w#((1.5-k_w)*w-(-0.5*w-k_w)*w)
    s = a*cos(2*angle)

    dx = s*cos(2*angle)
    dy = s*sin(2*angle)


    xs_1 = (s+dy)/(2*k)
    xs_2 = (s+dy)/(2*k)+dx
    ys_1 = (s+dy)/2
    ys_2 = (s-dy)/2

    xs = (xs_1+xs_2)/2
    ys = (ys_1+ys_2)/2

    xa = xs
    c1 = xa
    c2 = a - c1

    area_left_pts = [(0,0),
            (xa,0),
            (xs,ys),
            (xs_1, ys_1)]


    area_right_pts = [(xa,0),
            (a,0),
            (xs_2,ys_2),
            (xs,ys)]
    

    pts = [(0,0),
           (1.5*w, -1.5*h),
           ((1.5-k_w)*w, -2*h),
           ((-0.5-k_w)*w, -2*h),
           (-0.5*w, -1.5*h),
           (-w, -h)]

    #print(a, c1)
    #print(1.5*w, c2)

    max_wid = 2*(abs(max(1.5*w,-0.5-k_w))+c2) #((-0.5-k_w)*w)
    
    geo_xz = cq.Workplane("XZ").center(0,0).polyline(pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

    
    geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,0,tile_height))

    
    dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(max_wid, max_wid).extrude(-foundation_thickness))

    area_right_side = cq.Workplane("XZ").center((1.5-k_w)*w,0).polyline(area_left_pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)
    area_left_side = cq.Workplane("XZ").center((-0.5-k_w)*w-a,0).polyline(area_right_pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)


    circle_right_side = cq.Workplane("XZ").center((1.5-k_w)*w+c1,s/2).circle(s/2).extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

    circle_left_side = cq.Workplane("XZ").center((-0.5-k_w)*w-c2,s/2).circle(s/2).extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

    dog_side = dog_side.add(area_left_side).add(area_right_side)
    dog_side = dog_side.cut(circle_right_side).cut(circle_left_side)
    
    dog_side = dog_side.add(dog_side.translate((tile_len,0,0)))

    
    #circle = cq.Workplane("XZ").center(0.5*w+(tile_len/2-0.5*w)/2, 0).circle((tile_len/2-0.5*w)/2).extrude(tile_len*2+1).mirror(mirrorPlane="XZ", union=True)
    #circle = cq.Workplane("XZ").center(tile_len/2, 0).circle(0.1).extrude(tile_len)
    """
    circle = cq.Workplane("XZ").center(0.5*w+d/2, 0).circle(d/2).extrude(-(tile_wid+d)).mirror(mirrorPlane="XZ", union=True)
    
    dog_side = dog_side.cut(circle)

    extra_geo_xz = cq.Workplane("XZ").polyline(extra_pts).close().extrude(-(tile_wid+2*d)).translate((0, -d, 0))
    extra_geo_xy = cq.Workplane("XY").add(extra_geo_xz).translate((0,-tile_wid/2,tile_height))

    dog_side = dog_side.add(extra_geo_xy)
    """

    #exporters.export(geo_xy, "geo_xy.stl")

    return dog_side











ver = dog_side()#.center(0,0).circle(0.5).extrude(-6)
hor = dog_side().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))



def make_intersect(ver, hor):
    inter = ver.intersect(hor)

    return inter 



exporters.export(ver, "ver_dot.stl")
exporters.export(hor, "hor_dot.stl")

exporters.export(hor.add(ver), "union.stl")


"""
ver_half_left = dog_side().faces(">Y").workplane(-(tile_wid/2+d)).split(keepBottom=True)
ver_half_right = dog_side().faces(">Y").workplane(-(tile_wid/2+d)).split(keepTop=True)

hor_half_down = dog_side().rotate((0,0,0), (0,0,1), 90).faces(">X").workplane(-(tile_len/2+d)).split(keepBottom=True)
hor_half_up = dog_side().rotate((0,0,0), (0,0,1), 90).faces(">X").workplane(-(tile_len/2+d)).split(keepTop=True)


#corner_left_down = make_intersect(ver, hor).add(ver_half_left).add(hor_half_down)
#corner_left_up = make_intersect(ver, hor).add(ver_half_left).add(hor_half_up)
#corner_right_down = make_intersect(ver, hor).add(ver_half_right).add(hor_half_down)
corner_right_up = make_intersect(ver, hor).add(ver_half_right).add(hor_half_up)
circle_X = cq.Workplane("XZ").center(0.5*w+d/2, 0).workplane(offset=-(0.5*w+d/2)).circle(d/2).extrude(-(tile_len/2-0.5*w-d/2))

####circle_X = cq.Workplane("XZ").center(0.5*w+d/2, 0).workplane(offset=-(0.5*w)).circle(d/2).extrude(-(tile_len-0.5*w))

circle_Y = cq.Workplane("YZ").center(0.5*w+d/2, 0).workplane(offset=(0.5*w+d/2)).circle(d/2).extrude(tile_len/2-0.5*w-d/2)

corner_right_up = corner_right_up.cut(circle_X).cut(circle_Y)



#print(ver)
#print(hor)
exporters.export(ver, "ver_dot.stl")
exporters.export(hor, "hor_dot.stl")
#exporters.export(ver_half_left, "ver_half_left_dot.stl")
#exporters.export(hor_half_down, "hor_half_down_dot.stl")
#exporters.export(ver_half_right, "ver_half_right_dot.stl")
#exporters.export(hor_half_up, "hor_half_up_dot.stl")

#exporters.export(hor, "hor.stl")
#exporters.export(make_intersect(ver, hor), "inter_dot.stl")
#exporters.export(union, "union.stl")
#exporters.export(sub, "sub.stl")
#exporters.export(diff, "diff.stl")
#exporters.export(corner, "corner.stl")


#exporters.export(corner_left_down, "corner_left_down_dot.stl")
#exporters.export(corner_left_up, "corner_left_up_dot.stl")
#exporters.export(corner_right_down, "corner_right_down_dot.stl")
#exporters.export(corner_right_up, "corner_right_up_dot.stl")



#make dog leg in the middle extrude out to  
#cut ver and hor side parts and add them to intersect
#make a function to make thing if you want a deep copy
"""

