
import cadquery as cq
from cadquery import exporters
from wall_geometries_func import make_pyramid, make_block, add_foundation

tile_size = 1 # 1x1
tile_len = tile_size
tile_wid = tile_size
tile_height = 2
foundation_thickness = 4

def make_tria_side(tile_heigh=2, tile_len=1, tile_wid=1, foundation_thickness=4):
    """Make a triangular wall side facing y (upp/down or vertical) direction."""
    pts = [(0,0),
           (tile_len, 0),
           (tile_len/2, tile_height)]
    
    geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(tile_wid) #make wall

    geo_xy = cq.Workplane("XY").add(geo_xz) #change plane

    tria_side = geo_xy.faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #add foundation
    
    return tria_side

def make_tria_corner(ver, hor):
    """Make a triangular corner"""
    pass




    
def make_dogl_side():
    pass


def make_dogl_corner():
    pass



tria_side_ver = make_tria_side()
tria_side_hor = make_tria_side().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))
tria_corner = make_tria_corner(tria_side_ver, tria_side_hor)

exporters.export(tria_side_hor, "tria_side.stl")






#take in dir and out dir --> corner piece
#if dir upp or down --> ver else take hor
 
