import cadquery as cq
from cadquery import exporters



class Geometry():
    """Instance variables: position, geometry, base """
    
    def __init__(self, position=[0,0,0]):
        self.position = position
        
    
    def make_pyramid(self, base=[1.0, 1.0], height=2.0):
        """Creates a pyramid with parameters. Parameter base is the base area of pyramid,
           height is the height of pyramid and foundation is the thickness of the foundation below pyramid i XY plane."""
        
        self.geometry = (cq.Workplane("XY").rect(base[0],base[1]).workplane(offset=height).circle(0.001).loft(combine=True))

        self.base = base


    def make_block(self, base=[1.0, 1.0], height=2.0):
        """Creates a block with specified parameters and a foundation box.
           Parameters are base which is the block xy area, height of block and thickness of foundation under the block."""
        
        self.geometry = (cq.Workplane("XY").rect(base[0], base[1]).extrude(-height))

        self.base = base


    def add_foundation(self, thickness=4.0):
        """Add a foundation to selected geometry."""
        self.geometry.add(self.geometry.faces("<Z").rect(self.base[0],self.base[1]).extrude(-thickness))

    def move(self, step=[0,0,0]):
        """Move the geometry with step."""
        self.geometry = self.geometry.translate(step) #translate does not change geometry
        
    """
    def rotate(self, angle):
        self.geometry.rotate(angle)
    """ 


def unittest(): #manually checking
    geo = Geometry()
    geo.make_pyramid()
    geo.add_foundation()
    #geo.geometry.add(geo.geometry.faces("<Z").rect(1,1).extrude(-5))
    print(geo.geometry) #test if geometry is cq.Workplane
    
    geo2 = Geometry()
    geo2.make_pyramid()
    geo2.add_foundation()
    geo2.move([1,0,0]) #trying to translate geometry
    
    result = geo.geometry.add(geo2.geometry) #trying to add geometries together
    exporters.export(result, "geometry_move2.stl") #exporting to see if working correct


    #print(result)
    #exporters.export(result, "geometry_move2.stl")

#unittest()
