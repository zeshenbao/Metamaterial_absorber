
import cadquery as cq
from cadquery import exporters
from math import *


class Absorber():
    """Implements a absorber with patterns and different wall segments 
    and saved as a stl file.
    """

    def __init__(self, system, sides, corners, iterations):
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
        self.sides = sides
        self.corners = corners
        
        self.iterations = iterations
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
            self.result = cq.Workplane("XY").add(self.sides["hor"].translate((-1,0,0)))
        else:
            self.result = cq.Workplane("XY")
            
        
        for letter in self.system:

            #print(position[0], position[1], angle)
            
            if letter == "F":
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #return
                
                if angle == 0:
                    self.result.add(self.sides.hor.translate(position))
                    position[0] +=1

                elif angle == 180:
                    self.result.add(self.sides.hor.translate(position))
                    position[0] -=1
                    
                elif angle == 90:
                    self.result.add(self.sides.ver.translate(position))
                    position[1] -=1

                elif angle == 270:
                    self.result.add(self.sides.ver.translate(position))
                    position[1] +=1

                else:
                    print("error")

                
            elif letter == "+": #clockwise angle, + equals turn to the right or add 90 degrees
                if angle == 0:
                    #print(self.corners["left_down"])
                    self.result.add(self.corners["left_down"].translate(position))
                    position[1] -=1

                elif angle == 180:
                    self.result.add(self.corners["right_up"].translate(position))
                    position[1] +=1
                    
                elif angle == 90:
                    self.result.add(self.corners["left_up"].translate(position))
                    position[0] -=1

                elif angle == 270:
                    self.result.add(self.corners["right_down"].translate(position))
                    position[0] +=1

                else:
                    print("error")

                angle += 90
                angle %= 360
                
                
            elif letter == "-":
                if angle == 0:
                    self.result.add(self.corners["left_up"].translate(position))
                    position[1] +=1

                elif angle == 180:
                    self.result.add(self.corners["right_down"].translate(position))
                    position[1] -=1
                    
                elif angle == 90:
                    self.result.add(self.corners["right_up"].translate(position))
                    position[0] +=1

                elif angle == 270:
                    self.result.add(self.corners["left_down"].translate(position))
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
        block1 = self.sides
        block2 = self.sides.translate((1,0,0))
        
        exporters.export(self.result, "hilbert2.stl")


    def export(self, file_name):
        """Export created self.result to a stl file
        with file name specified with iterations."""
        print("exported")
        exporters.export(self.result, str(file_name) +str(self.iterations) +".stl")



class Store():
    def __init__(self, ver=None, hor=None, inter=None, ver_half_left=None, ver_half_right=None, hor_half_left=None, hor_half_right=None):
        self.ver = ver
        self.hor = hor
        self.inter =inter
        self.ver_half_left = ver_half_left
        self.ver_half_right = ver_half_right 
        self.hor_half_left =hor_half_left
        self.hor_half_right =hor_half_right
        
        


class Wall():
    """Implements different wall tiles such as sides
    and corner with different cross sections."""

    def __init__(self, tile_len=1.0, tile_wid=1.0, tile_height=2, foundation_thickness=4):
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

        self.sides = None
        self.corners = None


    def make_dog_components(self):
        """Make a triangular corner"""
         #carefull with rotation and see if they are at same position


        def copy_cross_section():
            foundation_thickness = 4
            h = self.tile_height/2
            angle = (pi/6)/2
            w = h*tan(angle)
            #print(w)
            pts = [(0,0),
                   (1.5*w, -1.5*h),

                   (0.5*w, -2*h),
                   (-1.5*w, -2*h),
                   (-0.5*w, -1.5*h),
                   (-w, -h)]

            #geo_xz, geo_xy, dog_side = None, None, None
            
            geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-self.tile_wid)

            geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,-self.tile_wid/2,self.tile_height))

            dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(self.tile_len, self.tile_wid).extrude(-foundation_thickness))


            return dog_side
            

        def copy_components():

            """
            comp = Store()
            comp.ver = copy_cross_section()
            comp.hor = copy_cross_section().rotate((0,0,0), (0,0,1), 90)
            #comp.inter = comp.ver.add(comp.hor)
            #exporters.export(ver, "ver2.stl")
            #exporters.export(hor, "hor2.stl")
            """
            

            """
            2.
            comp["ver"] = copy_cross_section()
            comp["hor"] = copy_cross_section().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))
            comp["inter"] = comp["ver"].add(comp["hor"])
            """
            
            """
            3.
            comp["ver"] = ver
            comp["hor"] = hor #((vek_svans),(vek_huvud),(grader))'
            comp["inter"] = comp["ver"].add(comp["hor"])
            """

            
            ver = copy_cross_section()
            hor = copy_cross_section().rotate((0,0,0), (0,0,1), 90)
            inter = ver.add(hor)
            
            exporters.export(ver, "ver4.stl")
            exporters.export(hor, "hor4.stl")

            stop()
            
            return comp



        def copy_sides():
            comp = Store()
            
            comp.ver_half_left = copy_components().ver.faces(">Y").workplane(-0.5).split(keepBottom=True)
            comp.ver_half_right = copy_components().ver.faces(">Y").workplane(-0.5).split(keepTop=True)

            comp.hor_half_down = copy_components().hor.faces(">X").workplane(-0.5).split(keepBottom=True)
            comp.hor_half_up = copy_components().hor.faces(">X").workplane(-0.5).split(keepTop=True)

            return comp
        
        sides = copy_sides()

        #exporters.export(copy_components()["ver"], "ver.stl")
        #exporters.export(copy_components()["hor"], "hor.stl")
        corners = {}


        corners["left_down"] = copy_components().inter.add(sides.ver_half_left).add(sides.hor_half_down)
        corners["left_up"] = copy_components().inter.add(sides.ver_half_left).add(sides.hor_half_up)
        corners["right_down"] = copy_components().inter.add(sides.ver_half_right).add(sides.hor_half_down)
        corners["right_up"] = copy_components().inter.add(sides.ver_half_right).add(sides.hor_half_up)
        

        #exporters.export(corner, "testing_corner.stl")
        
        
        exporters.export(sides.ver_half_left, "ver_half_left.stl")
        exporters.export(sides.ver_half_right, "ver_half_right.stl")
        exporters.export(sides.hor_half_down, "hor_half_down.stl")
        exporters.export(sides.hor_half_up, "hor_half_up.stl")


        exporters.export(corners["left_down"], "corner_left_down.stl")
        exporters.export(corners["left_up"], "corner_left_up.stl")
        exporters.export(corners["right_down"], "corner_right_down.stl")
        exporters.export(corners["right_up"], "corner_right_up.stl")

        
        return copy_components(), corners



def generate_hilbert(iterations):
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
    #print(system)

    return system



def main():
    """Operates functions and classes to export a finished stl file."""

    iterations = 3
    
    hilbert = generate_hilbert(iterations)

    dogleg_wall = Wall()
    dogleg_sides, dogleg_corners = dogleg_wall.make_dog_components()
    #unittest()
    hilbert_absorber = Absorber(hilbert, dogleg_sides, dogleg_corners, iterations)
    hilbert_absorber.build()
    hilbert_absorber.export("hilbert_dog_face_fix_")
    




#if __name__ == "main":
main()







