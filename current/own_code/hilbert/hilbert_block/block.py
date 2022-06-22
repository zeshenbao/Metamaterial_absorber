import cadquery as cq
from cadquery import exporters

def block(base=(1.0,1.0), height=2.0, foundation =0.5):
    """Creates a block with specified parameters and a foundation box.
       Parameters are base which is the block xy area, height of block and
       thickness of foundation under the block."""
    
    return (cq.Workplane("XY").rect(base[0],base[1]).extrude(foundation)
            .faces(">Z").rect(base[0],base[1]).rect(base[0], base[1]).extrude(height)
    )

#exporters.export(block(),"block.stl")
    
