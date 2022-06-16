
import cadquery as cq
from cadquery import exporters
from wall_geometries_func import make_pyramid, make_block, add_foundation

tile_size = 1 # 1x1
tile_len = tile_size
tile_wid = tile_size
tile_height = 2
foundation_thickness = 4

def make_tria_side(tile_height=2, tile_len=1, tile_wid=1, foundation_thickness=4):
    """Make a triangular wall side facing y (upp/down or vertical) direction."""
    pts = [(0,0),
           (tile_len, 0),
           (tile_len/2, tile_height)]
    
    geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-tile_wid) #make wall

    geo_xy = cq.Workplane("XY").add(geo_xz) #change plane

    tria_side = geo_xy.faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #add foundation
    tria_side_ver = tria_side
    tria_side_hor = tria_side.rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,1), 90) #((vek_svans),(vek_huvud),(grader))

    return [tria_side_ver, tria_side_hor]


def make_sub(tile_height=2, tile_len=1, tile_wid=1, foundation_thickness=4):
    """Make the element to remove from union before adding with intersection """
    pts = [(tile_len, 0),
           (tile_len, tile_wid),
           (0, tile_wid)
        ]
    
    sub = cq.Workplane("XY").polyline(pts).close().extrude(tile_height)#.faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #skapas vid masspunkt
    
    return sub

def make_tria_corner(side, sub):
    """Make a triangular corner"""
    ver = side[0]
    hor = side[1]
    inter = ver.intersect(hor) #carefull with rotation and see if they are at same position
    union = ver.add(hor)
    sub = union.cut(sub)
    corner = sub.add(inter)
    
    return corner



    
def make_dogl_side():
    pass


def make_dogl_corner():
    pass


tria_side_ver, tria_side_hor = make_tria_side()
#exporters.export(tria_side_ver, "tria_corner_ver.stl")
#exporters.export(tria_side_hor, "tria_corner_hor.stl")


sub = make_sub()
#exporters.export(remove, "remove.stl")

                          
tria_corner_left_down = make_tria_corner(make_tria_side(), sub)
tria_corner_left_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 90)
tria_corner_right_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 180)
tria_corner_right_down = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 270)

"""
exporters.export(tria_corner_left_down, "tria_corner_left_down.stl")
exporters.export(tria_corner_left_up, "tria_corner_left_up.stl")
exporters.export(tria_corner_right_up, "tria_corner_right_up.stl")
exporters.export(tria_corner_right_down, "tria_corner_right_down.stl")
"""


#take in dir and out dir --> corner piece
#if dir upp or down --> ver else take hor
 
