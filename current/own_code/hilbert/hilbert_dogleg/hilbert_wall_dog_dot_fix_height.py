
import cadquery as cq
from cadquery import exporters
from math import *


class Absorber():
    """Implements a absorber with patterns and different wall segments 
    and saved as a stl file.
    """

    def __init__(self, system, sides, corners, iterations, scale):
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
        self.scale = scale

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
            self.result = cq.Workplane("XY").add(self.sides["hor"].translate((-1*self.scale,0,0)))
        else:
            self.result = cq.Workplane("XY")
            
        
        for letter in self.system:

            #print(position[0], position[1], angle)
            
            if letter == "F":
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #return
                
                if angle == 0:
                    self.result.add(self.sides["hor"].translate(position))
                    position[0] +=1*self.scale

                elif angle == 180:
                    self.result.add(self.sides["hor"].translate(position))
                    position[0] -=1*self.scale
                    
                elif angle == 90:
                    self.result.add(self.sides["ver"].translate(position))
                    position[1] -=1*self.scale

                elif angle == 270:
                    self.result.add(self.sides["ver"].translate(position))
                    position[1] +=1*self.scale

                else:
                    print("error")

                
            elif letter == "+": #clockwise angle, + equals turn to the right or add 90 degrees
                if angle == 0:
                    #print(self.corners["left_down"])
                    self.result.add(self.corners["left_down"].translate(position))
                    position[1] -=1*self.scale

                elif angle == 180:
                    self.result.add(self.corners["right_up"].translate(position))
                    position[1] +=1*self.scale
                    
                elif angle == 90:
                    self.result.add(self.corners["left_up"].translate(position))
                    position[0] -=1*self.scale

                elif angle == 270:
                    self.result.add(self.corners["right_down"].translate(position))
                    position[0] +=1*self.scale

                else:
                    print("error")

                angle += 90
                angle %= 360
                
                
            elif letter == "-":
                if angle == 0:
                    self.result.add(self.corners["left_up"].translate(position))
                    position[1] +=1*self.scale

                elif angle == 180:
                    self.result.add(self.corners["right_down"].translate(position))
                    position[1] -=1*self.scale
                    
                elif angle == 90:
                    self.result.add(self.corners["right_up"].translate(position))
                    position[0] +=1*self.scale

                elif angle == 270:
                    self.result.add(self.corners["left_down"].translate(position))
                    position[0] -=1*self.scale

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



class Wall():
    """Implements different wall tiles such as sides
    and corner with different cross sections."""

    def __init__(self, tile_len=1.0, tile_wid=1.0, tile_height=2, foundation_thickness=4, scale=2):
        """Creates a wall object.
        :param tile_len: length of tile
        :param tile_wid: width of tile
        :param tile_height: height of tile
        :param foundation_thickness: thickness of the tile foundation under the cross section.
        """
        self.scale = scale
        self.tile_len = tile_len * self.scale
        self.tile_wid = tile_wid * self.scale
        self.tile_height = tile_height * self.scale
        self.foundation_thickness = foundation_thickness *self.scale

        self.sides = None
        self.corners = None

    def get_scale(self):
        return self.scale

    def make_dog_components(self):
        """Make a triangular corner"""
         #carefull with rotation and see if they are at same position


        def copy_cross_section():
            foundation_thickness = self.foundation_thickness
            h = self.tile_height/2
            angle = (pi/6)/2
            self.w = h*tan(angle)
            self.d = self.tile_len - 0.5*self.w - 1.5*self.w
            x = (self.d/2)*tan(2*angle)
            #print(w)
            pts = [(0,0),
                   (1.5*self.w, -1.5*h),
                   (0.5*self.w, -2*h),
                   (-1.5*self.w, -2*h),
                   (-0.5*self.w, -1.5*h),
                   (-self.w, -h)]

            extra_pts = [(-1.5*self.w, -2*h),
                 (0.5*self.w, -2*h),
                 (0.5*self.w-x, -2*h-self.d/2),
                 (-1.5*self.w-x, -2*h-self.d/2)]

            #geo_xz, geo_xy, dog_side = None, None, None
            
            geo_xz = cq.Workplane("XZ").polyline(pts).close().extrude(-(self.tile_wid+2*self.d)).translate((0, -self.d, 0)) #add twp stick out part and then shift with one shift out to get one shift out part every side.

            geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,-self.tile_wid/2,self.tile_height))

            dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(self.tile_len, self.tile_wid).extrude(-self.foundation_thickness))

            circle = cq.Workplane("XZ").center(0.5*self.w+self.d/2, 0).circle(self.d/2).extrude(-(self.tile_wid+self.d)).mirror(mirrorPlane="XZ", union=True)
    
            dog_side = dog_side.cut(circle)

            #extension
            extra_geo_xz = cq.Workplane("XZ").polyline(extra_pts).close().extrude(-(self.tile_wid+2*self.d)).translate((0, -self.d, 0))
            extra_geo_xy = cq.Workplane("XY").add(extra_geo_xz).translate((0,-self.tile_wid/2,self.tile_height))

            dog_side = dog_side.add(extra_geo_xy)


            return dog_side
            

        def copy_components():
            comp = {}
            comp["ver"] = copy_cross_section()
            comp["hor"] = copy_cross_section().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))
            comp["inter"] = comp["ver"].intersect(comp["hor"]) ### the start workplane must always be new but add could be reused
            return comp

        def copy_sides(comp):
            sides = {}
            
            sides["ver_half_left"] = comp["hor"].faces(">X").workplane(-(self.tile_len/2+self.d)).split(keepBottom=True)
            sides["ver_half_right"] = comp["hor"].faces(">X").workplane(-(self.tile_len/2+self.d)).split(keepTop=True)

            sides["hor_half_down"] = comp["ver"].faces(">Y").workplane(-(self.tile_wid/2+self.d)).split(keepBottom=True)
            sides["hor_half_up"] = comp["ver"].faces(">Y").workplane(-(self.tile_wid/2+self.d)).split(keepTop=True)
            

            return sides
        
        sides = copy_sides(copy_components())

        exporters.export(copy_components()["ver"], "ver.stl")
        exporters.export(copy_components()["hor"], "hor.stl")
        corners = {}


        corners["left_down"] = copy_components()["inter"].add(sides["ver_half_left"]).add(sides["hor_half_down"]) 
        corners["left_up"] = copy_components()["inter"].add(sides["ver_half_left"]).add(sides["hor_half_up"])      #
        corners["right_down"] = copy_components()["inter"].add(sides["ver_half_right"]).add(sides["hor_half_down"]) #
        corners["right_up"] = copy_components()["inter"].add(sides["ver_half_right"]).add(sides["hor_half_up"])

        circle_X = cq.Workplane("XZ").center(0.5*self.w+self.d/2, 0).workplane(offset=-(0.5*self.w+self.d/2)).circle(self.d/2).extrude(-(self.tile_len/2-0.5*self.w-self.d/2))
        circle_Y = cq.Workplane("YZ").center(0.5*self.w+self.d/2, 0).workplane(offset=(0.5*self.w+self.d/2)).circle(self.d/2).extrude(self.tile_len/2-0.5*self.w-self.d/2)

        corners["right_up"] = corners["right_up"].cut(circle_X).cut(circle_Y)


        #exporters.export(corner, "testing_corner.stl")
        exporters.export(copy_components()["inter"], "inter.stl")
        
        exporters.export(sides["ver_half_left"], "ver_half_left.stl")
        exporters.export(sides["ver_half_right"], "ver_half_right.stl")
        exporters.export(sides["hor_half_down"], "hor_half_down.stl")
        exporters.export(sides["hor_half_up"], "hor_half_up.stl")

 
        exporters.export(corners["left_down"], "corner_left_down.stl")
        exporters.export(corners["left_up"], "corner_left_up.stl")
        exporters.export(corners["right_down"], "corner_right_down.stl")
        exporters.export(corners["right_up"], "corner_right_up.stl")

        
        return copy_components(), corners


    

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


def unittest():
    #the tests are made manually with visually checking exported stl files.
    exporters.export(triangle_sides["ver"], "ver.stl")
    exporters.export(triangle_sides["hor"], "hor.stl")
    
    exporters.export(triangle_corners["left_down"], "left_down.stl")
    exporters.export(triangle_corners["left_up"], "left_up.stl")
    exporters.export(triangle_corners["right_up"], "right_up.stl")
    exporters.export(triangle_corners["right_down"], "right_down.stl")
    


def main():
    """Operates functions and classes to export a finished stl file."""

    iterations = 2
    
    hilbert = generate_hilbert(iterations)

    dogleg_wall = Wall(foundation_thickness=1, tile_height=3)
    dogleg_sides, dogleg_corners = dogleg_wall.make_dog_components()
    scale = dogleg_wall.get_scale()
    #unittest()
    hilbert_absorber = Absorber(hilbert, dogleg_sides, dogleg_corners, iterations, scale)
    hilbert_absorber.build()
    hilbert_absorber.export("hilbert_dog_face_dot_")
    




#if __name__ == "main":
main()







