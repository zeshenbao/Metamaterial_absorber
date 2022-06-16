
import cadquery as cq
from cadquery import exporters



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


class Pattern():
    """
    Used to generate a pattern with desired cross section in 3d.
    
    :param side: wall section for straight paths.
    :param corner: corner section of the wall.
    :param system: L-system to generate the walls.
    """

    def __init__(self, iterations, side_ver, side_hor, corner_left_down, corner_left_up, corner_right_up, corner_right_down):

        self.iterations = iterations
        self.side_ver = side_ver
        self.side_hor = side_hor
        self.corner_left_down = corner_left_down
        self.corner_left_up = corner_left_up
        self.corner_right_up = corner_right_up
        self.corner_right_down = corner_right_down
        self.system = self.L_system(self.iterations)

    def L_system(self, iterations):
        axiom = "A"
        A = "+BF-AFA-FB+"
        B = "-AF+BFB+FA-"

        system = axiom

        for i in range(iterations):
            system = system.replace("A", "a").replace("B", "b") #a, b are temporary variables because we wnt to replace A and B at the same time

            system = system.replace("a", A).replace("b", B)

        system = system.replace("A", "").replace("B", "")
        
        while "+-" in system:
            system = system.replace("+-", "")
            
        while "-+" in system:
            system = system.replace("-+", "")

        system = system.replace("F+", "+").replace("F-", "-")

        return system

    
    def generate_pattern(self): #0pi == right
        position = [0,0,0]
        angle = 0
        if self.iterations % 2 == 0:
            self.result = cq.Workplane("XY").add(tria_side_hor.translate((-1,0,0)))
        else:
            self.result = cq.Workplane("XY")
        count = 0
        
        for letter in self.system:
            """
            if self.system[0] == "+":
                angle += 90
                angle %= 360
                pass 

            elif self.system[0] == "-":
                angle -= 90
                angle %= 360
                pass
            """
            print(position[0], position[1], angle)
            
            if letter == "F":
                if angle == 0:
                    self.result.add(tria_side_hor.translate(position))
                    position[0] +=1

                elif angle == 180:
                    self.result.add(tria_side_hor.translate(position))
                    position[0] -=1
                    
                elif angle == 90:
                    self.result.add(tria_side_ver.translate(position))
                    position[1] -=1

                elif angle == 270:
                    self.result.add(tria_side_ver.translate(position))
                    position[1] +=1

                else:
                    print("error")

                
            elif letter == "+": #clockwise angle
                if angle == 0:
                    self.result.add(tria_corner_left_down.translate(position))
                    position[1] -=1

                elif angle == 180:
                    self.result.add(tria_corner_right_up.translate(position))
                    position[1] +=1
                    
                elif angle == 90:
                    self.result.add(tria_corner_left_up.translate(position))
                    position[0] -=1

                elif angle == 270:
                    self.result.add(tria_corner_right_down.translate(position))
                    position[0] +=1

                else:
                    print("error")

                angle += 90
                angle %= 360
                
                
            elif letter == "-":
                if angle == 0:
                    self.result.add(tria_corner_left_up.translate(position))
                    position[1] +=1

                elif angle == 180:
                    self.result.add(tria_corner_right_down.translate(position))
                    position[1] -=1
                    
                elif angle == 90:
                    self.result.add(tria_corner_right_up.translate(position))
                    position[0] +=1

                elif angle == 270:
                    self.result.add(tria_corner_left_down.translate(position))
                    position[0] -=1

                else:
                    print("error")

                angle -= 90
                angle %= 360
                
            count += 1
            #if count == 1:
                #position[2] += 1

            
            

                
        print(self.system)
        self.export()


    
    def test(self):
        block1 = self.side
        block2 = self.side.translate((1,0,0))
        
        exporters.export(self.result, "hilbert2.stl")

    def export(self):
        exporters.export(self.result, "hilbert.stl")



tria_side_ver, tria_side_hor = make_tria_side()


sub = make_sub()

### write better code                           
tria_corner_left_down = make_tria_corner(make_tria_side(), sub)
tria_corner_left_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 90)
tria_corner_right_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 180)
tria_corner_right_down = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 270)


hilbert = Pattern(6, tria_side_ver, tria_side_hor, tria_corner_left_down, tria_corner_left_up, tria_corner_right_up, tria_corner_right_down)

hilbert.generate_pattern()
