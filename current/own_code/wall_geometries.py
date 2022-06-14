import cadquery as cq
from cadquery import exporters



class Geometry():

    def __init__(self)
    
    def pyramid(base=(1,1), height=1, foundation = 0.5):
        """Creates a pyramid with parameters. Parameter base is the base area of pyramid,
           height is the height of pyramid and foundation is the thickness of the foundation below pyramid i XY plane."""
        
        return (cq.Workplane("XY").rect(base[0],base[1]).extrude(foundation)
                .faces(">Z").rect(base[0],base[1]).workplane(offset=height).circle(0.001).loft(combine=True))


    def block(base=(1.0,1.0), height=2.0, foundation =0.5):
        """Creates a block with specified parameters and a foundation box.
           Parameters are base which is the block xy area, height of block and thickness of foundation under the block."""
        
        return (cq.Workplane("XY").rect(base[0], base[1]).extrude(-height))


    def foundation(geometry, thickness=0.5):
        """Add a foundation to selected geometry."""
        return (geometry.faces("<Z").rect(base[0]+1,base[1]+1).extrude(-foundation))


exportes.export(foundation)
