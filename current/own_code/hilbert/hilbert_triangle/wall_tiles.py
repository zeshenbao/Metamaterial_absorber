
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
    pts = [(-tile_len/2,0),
           (tile_len/2, 0),
           (0, tile_height)]
    
    geo_xz = cq.Workplane("XZ").tag("baseplane").polyline(pts).close().extrude(-tile_wid).workplaneFromTagged("baseplane").extrude(tile_wid) #make wall

    geo_xy = cq.Workplane("XY").add(geo_xz) #change plane

    tria_side = geo_xy.faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #add foundation
    
    return tria_side


def make_remove(tile_height=2, tile_len=1, tile_wid=1, foundation_thickness=4):
    """Make the element to remove from union before adding with intersection """
    pts = [(tile_len/2, -tile_wid/2),
           (tile_len/2, tile_wid/2),
           (-tile_len/2, tile_wid)
        ]
    
    remove = cq.Workplane("XY").polyline(pts).close().extrude(tile_height).faces("<Z").rect(tile_len, tile_wid).extrude(-foundation_thickness) #extrudes at neg direction??
    
    return remove

def make_tria_corner(ver, hor, remove):
    """Make a triangular corner"""
    inter = ver.intersect(hor) #carefull with rotation and see if they are at same position
    union = ver.add(hor)
    sub = union.cut(remove)
    #corner = sub.add(inter)

    exporters.export(sub, "sub.stl")
    
    #return corner




    
def make_dogl_side():
    pass


def make_dogl_corner():
    pass



tria_side_ver = make_tria_side()
tria_side_hor = make_tria_side().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))
exporters.export(tria_side_ver, "tria_corner_ver.stl")
#exporters.export(tria_side_hor, "tria_corner_hor.stl")


remove = make_remove()
#exporters.export(remove, "remove.stl")

                          
#tria_corner = make_tria_corner(tria_side_ver, tria_side_hor, remove) 
#exporters.export(tria_corner, "tria_corner.stl")



#take in dir and out dir --> corner piece
#if dir upp or down --> ver else take hor
 
