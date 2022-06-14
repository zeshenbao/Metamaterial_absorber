
#Write code for pattern
#Write class for absorber objects


#make a pyramid
#make a s-shape with several pyramids
#make a pattern with pyramids


import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO



class Generator():
    """Creates a cotroller class to generate patterns."""

    def __init__(self, absorber):
        """ """
        self.absorber = absorber

    def pattern(self, iterations):
        """Generate a pattern to put the input absorber.

           :param absorber: Absorber object, cq.CD (dots for now)
           :param iterations: int
           
           return: a cadquery result with combined absorbers elements. (red/blue dots for now)
        """
        pass

    def corner(self):
        """ Generate corner
        """
        pass



class Point():
    """Stores coordinates for a point."""
    def __init__(self, x, y, z):
        """Creates a point object.

           :param x: int
           :param y: int
           :param z: int

           return: None
        """
        self.x = x
        self.y = y
        self.z = z
        
        
class Absorber():
    """An absorber object which is dog_leg for now."""
    
    def __init__(self, position=Point(0,0,0), scale=1, length=2, width=1, height=1, angle=0):
        """Creates the absorber object.

           :param position: Point type, position of object
           :param scale: float
           :param height: float
           :param width: float
           :param depth: int
           :param angle: float
           
           return: None
        """
        #other cad parts
        
        self.position = position
        self.scale = scale
        self.length = length
        self.width = width
        self.height = height
        self.angle = angle
        
        

    def build(self):
        """ Builds the shape of absorber from different parts.
        """
        pass
    
    def part1(self):
        """ Creates the first part from cq
        """
        pass

    def part2(self):
        """
        """
        pass



def export(result, file_type):
    """Exports the generated pattern to step/stl file, return None.
    """
    #exporters.export(result, "tester5." +str(file_type))


def main():
    box = cq.Workplane("XY").box(3,3,5)

    export(box, "tester5.stl")
    print("done")
    #show_object(box)


if __name__ == "__main__":
    main()












    




        
