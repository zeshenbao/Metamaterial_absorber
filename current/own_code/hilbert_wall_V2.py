
import cadquery as cq
from cadquery import exporters





class Absorber():
    """Implements a absorber with patterns and different wall segments 
    and saved as a stl file.
    """

    def __init__(self, system, corners, sides):
        """Creates an absorber object with input wall corners, wall sides and system.
         _____ _____    ___________
        |     |     |  |           |    
        |  2  |  3  |  |           |   
        |-----+-----|  |     +-----|    
        |  1  |  0  |  |     |  1  |
        |_____|_____|, |_____|_____|     
      
        
        :param corners: A dictionary that stores wall corner in 4 different directions as seen in the figure above.
        You can see how the zeroth list element looks like.

        :param sides: A dictionary of two wall sides, the zeroth vertically and first horisontal.

        :param result: The generated absorber as a cq.Workplane object.

        """

        self.system = system
        self.corners = corners
        self.sides = sides
        self.result = None

    def build(self): 
        """Builds the absorber with instance variables."""
        
        """Code variable reminders:
           :var pos: position of current tile
           :var angle: current direction of movement of the tile.
           :var count: current tile number.
        """
        position = [0,0,0]
        angle = 0    #0 degrees == right
        count = 0

        
        if self.iterations % 2 == 0:
            self.result = cq.Workplane("XY").add(sides[0].translate((-1,0,0)))
        else:
            self.result = cq.Workplane("XY")
            
        
        for letter in self.system:

            #print(position[0], position[1], angle)
            
            if letter == "F":
                if angle == 0:
                    self.result.add(sides["hor"].translate(position))
                    position[0] +=1

                elif angle == 180:
                    self.result.add(sides["hor"].translate(position))
                    position[0] -=1
                    
                elif angle == 90:
                    self.result.add(sides["ver"].translate(position))
                    position[1] -=1

                elif angle == 270:
                    self.result.add(sides["ver"].translate(position))
                    position[1] +=1

                else:
                    print("error")

                
            elif letter == "+": #clockwise angle, + equals turn to the right or add 90 degrees
                if angle == 0:
                    self.result.add(corners["left_down"].translate(position))
                    position[1] -=1

                elif angle == 180:
                    self.result.add(corners["right_up"].translate(position))
                    position[1] +=1
                    
                elif angle == 90:
                    self.result.add(corners["left_up"].translate(position))
                    position[0] -=1

                elif angle == 270:
                    self.result.add(corners["right_down"].translate(position))
                    position[0] +=1

                else:
                    print("error")

                angle += 90
                angle %= 360
                
                
            elif letter == "-":
                if angle == 0:
                    self.result.add(corners["left_up"].translate(position))
                    position[1] +=1

                elif angle == 180:
                    self.result.add(corners["right_down"].translate(position))
                    position[1] -=1
                    
                elif angle == 90:
                    self.result.add(corners["right_up"].translate(position))
                    position[0] +=1

                elif angle == 270:
                    self.result.add(corners["left_down"].translate(position))
                    position[0] -=1

                else:
                    print("error")

                angle -= 90
                angle %= 360
                
            count += 1
            #if count == 1: #check first block
                #position[2] += 1

    def test(self):
        """Used to test different builds."""
        block1 = self.side
        block2 = self.side.translate((1,0,0))
        
        exporters.export(self.result, "hilbert2.stl")


    def export(self):
        """Export created self.result to a stl file
        with file name specified with iterations."""
        
        exporters.export(self.result, "hilbert_iter" +str(self.iterations) +".stl")



class Wall():
    """Implements different wall tiles such as sides
    and corner with different cross sections."""

    def __init__(self, tile_len=1, tile_wid=1, tile_height=2, foundation_thickness=4):
        """Creates a wall object.
        :param tile_len: length of tile
        :param tile_wid: width of tile
        :param tile_height: height of tile
        :param foundation_thickness: thickness of the tile foundation under the cross section.
        """
        self.tile_len = tile_len
        self.tile_wid = tile_wid
        self.tile_height = tile_height
        self.foundation_thickness = foundation_thickness


    def make_tria_side(self):
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


    def make_sub(self):
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
        diff = union.cut(sub)
        corner = diff.add(inter)
        
        return corner




#class Pattern(): #Probably don't need a class for this, might need it for later
#    """
#    #Used to generate different patterns.
#
#    :param system: System instructions to generate the walls.
#    """
#
#    def __init__(self):
#        """Creates a pattern object with an empty system."""
#        self.system = None



def generate_hilbert(self, iterations):
    """Generates and returns a hilbert curve system 
    where the iterations depends on the parameter iterations. 

    :param iterations: iterations of hilbert system.
    """
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

    #self.system = system
    print(self.system)

    return system


def unittest():
    #the tests are made manually with visually checking exported stl files.
    pass


def main():
    """Operates functions and classes to export a finished stl file."""




if __name__ == "main":
    main()











tria_side_ver, tria_side_hor = make_tria_side()


sub = make_sub()

### write better code                           
tria_corner_left_down = make_tria_corner(make_tria_side(), sub)
tria_corner_left_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 90)
tria_corner_right_up = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 180)
tria_corner_right_down = make_tria_corner(make_tria_side(), sub).rotate((tile_len/2,tile_wid/2,0), (tile_len/2,tile_wid/2,-1), 270)


hilbert = Pattern(7, tria_side_ver, tria_side_hor, tria_corner_left_down, tria_corner_left_up, tria_corner_right_up, tria_corner_right_down)

hilbert.generate_pattern()
