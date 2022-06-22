import cadquery as cq
from cadquery import exporters
from wall_geometries_func import make_pyramid, make_block, add_foundation


class Pattern():
    """
    Used to generate a pattern with desired cross section in 3d.
    
    :param side: wall section for straight paths.
    :param corner: corner section of the wall.
    :param system: L-system to generate the walls.
    """

    def __init__(self, iterations, cross_section = add_foundation(make_block())):
        self.side = cross_section
        self.corner = cross_section
        self.system = L_system(iterations)

    def L_system(iterations):
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

        return system

    """
    def generate_pattern(self): #0pi == right
        position = [0,0,0]
        angle = 0
        
        for letter in system:
            
            if letter == "F":
                
            elif letter == "+":
                
            elif letter == "-":
    """
    def test(self):
        block1 = self.side
        block2 = self.side.translate((1,0,0))
        
        exporters.export(result, "hilbert2.stl")

    def export(self):
        exporters.export(result, "hilbert.stl")























