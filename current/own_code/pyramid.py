import cadquery as cq
from cadquery import exporters



def pyramid(base=(1,1), height=1, foundation = 0.5):
    """Creates a pyramid with parameters. Parameter base is the base area of pyramid,
       height is the height of pyramid and foundation is the thickness of the foundation below pyramid i XY plane."""
    
    #return (cq.Workplane("XY").rect(base[0], base[1]).workplane(offset=height).circle(0.001).loft(combine=True))
    return base = (cq.Workplane("XY").rect(base[0],base[1]).extrude(foundation)
                   .faces(">Z").rect(base[0],base[1]).workplane(offset=height).circle(0.001).loft(combine=True))



#exporters.export(pyramid((2,2),1), "pyra_XY.stl")
