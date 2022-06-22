
#Write code for pattern
#Write class for absorber objects



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

           param absorber: Absorber object: cq.CD (dots for now)
           param iterations: int
           
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

           Parameters
           ----------
           x: int
           y: int
           z: int

           return: None
        """
        self.x = x
        self.y = y
        self.z = z
        
        
class Absorber():
    """An absorber object which is dog_leg for now."""
    
    def __init__(self, position, scale, height, width, angle, depth):
        """Creates the absorber object.

           Parameters
           ----------
           position: Point
           scale: float
           height: float
           width: float
           depth: int
           angle: float
           
           return: None
        """
        #other cad parts
        
        self.position = position
        self.scale = scale
        self.height = height
        self.width = width
        self.angle = angle
        self.thickness = thickness
        

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





def main():
    exporters.export(result, "tester3." +str(file_type))

def __name__ == "__main__":
    main()






        
