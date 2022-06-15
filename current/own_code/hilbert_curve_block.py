import cadquery as cq
from cadquery import exporters
from wall_geometries_func import make_pyramid, make_block, add_foundation


class Pattern():
    """
    :param direction: direction 
    """

    def __init__(self, iterations, cross_section = add_foundation(make_block())):
        self.side = cross_section
        self.corner = cross_section
        self.system = L_system(iterations)

    def L_system(self, iterations):
        axiom = "A"
        A = "+BF−AFA−FB+"
        B = "−AF+BFB+FA−"

        system = axiom

        for i in range(iterations):
            system = system.replace("A", "a") #a, b are temporary variables because we wnt to replace A and B at the same time
            system = system.replace("B", "b")

            system = system.replace("a", "+BF−AFA−FB+")
            system = system.replace("b", "−AF+BFB+FA−")

        system = system.replace("A", "")
        system = system.replace("B", "")

        return system

    """
    def generate_pattern(self, direction = "right"):
        for letter in system:
            match "+"
            "-"
            "F"
        
    """

    def export(self):
        exporters.export(result, "hilbert.stl")




