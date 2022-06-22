import cadquery as cq
from cadquery import exporters


def make_pyramid(base=(1.0, 1.0), height=1.0):
    """Creates a pyramid with parameters. Parameter base is the base area of pyramid,
       height is the height of pyramid and foundation is the thickness of the foundation below pyramid i XY plane."""
    
    return (cq.Workplane("XY").rect(base[0],base[1]).workplane(offset=height).circle(0.001).loft(combine=True))


def make_block(base=(1.0, 1.0), height=2.0):
    """Creates a block with specified parameters and a foundation box.
       Parameters are base which is the block xy area, height of block and thickness of foundation under the block."""
    
    return (cq.Workplane("XY").rect(base[0], base[1]).extrude(-height))


def add_foundation(geometry, base=(1.0, 1.0), thickness=3.0):
    """Add a foundation to selected geometry."""
    return (geometry.faces("<Z").rect(base[0],base[1]).extrude(-thickness))



"""
pyramid = add_foundation(make_pyramid())
pyr2 = add_foundation(make_pyramid()).translate((1,0,0))
result = pyramid.add(pyr2)
exporters.export(result, "pyramid_func2.stl")
"""
