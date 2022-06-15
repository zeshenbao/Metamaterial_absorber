import cadquery as cq
from cadquery import exporters



class Geometry():

    def __init__(self, position=[0,0,0]):
        self.position = position
        
    
    def pyramid(self, base=(1.0, 1.0), height=1.0, foundation=3.0):
        """Creates a pyramid with parameters. Parameter base is the base area of pyramid,
           height is the height of pyramid and foundation is the thickness of the foundation below pyramid i XY plane."""
        
        self.geometry = (cq.Workplane("XY").rect(base[0],base[1]).extrude(foundation)
                .faces(">Z").rect(base[0],base[1]).workplane(offset=height).circle(0.001).loft(combine=True))

        self.base = base


    def block(self, base=(1.0, 1.0), height=2.0, foundation=3.0):
        """Creates a block with specified parameters and a foundation box.
           Parameters are base which is the block xy area, height of block and thickness of foundation under the block."""
        
        self.geometry = (cq.Workplane("XY").rect(base[0], base[1]).extrude(-height))

        self.base = base


    def add_foundation(self, thickness=3.0):
        """Add a foundation to selected geometry."""
        return (self.geometry.faces("<Z").rect(self.base[0],self.base[1]).extrude(-thickness))



def unittest():
    geo = Geometry()
    geo.pyramid()
    geo.add_foundation()

    print(cq.Location())

    #exporters.export(geo.geometry, "geometry3.stl")

unittest()
