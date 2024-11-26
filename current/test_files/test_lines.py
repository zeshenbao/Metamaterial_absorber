import cadquery as cq
from cadquery import exporters

"""
result = (cq.Workplane("XY")
          # create a triangular prism and tag it
          .polygon(3, 100).extrude(4).tag("prism"))
"""



# 1.make a cross section in "XZ"
# 2.extrude
# 3.cq.Workplane("XY").add(section)

"""
tilt = cq.Workplane("XZ").rect(1,2).extrude(1)

block = cq.Workplane("XY").add(tilt) #.faces("<Z").extrude(-foundation)

block1 = block 
block2 = block.translate((1,0,0))
block3 = block.translate((2,0,0))
block4 = block.translate((2,1,0))

result = block1.add(block2).add(block3).add(block4)
exporters.export(result, "prism.stl")
"""

tilt = cq.Workplane("XZ").polygon(3,1).extrude(1)

block = cq.Workplane("XY").add(tilt) #.faces("<Z").extrude(-foundation)

block1 = block 
block2 = block.translate((1,0,0))
block3 = block.translate((2,0,0))
block4 = block.translate((2,1,0))

result = block1.add(block2).add(block3).add(block4)
exporters.export(result, "prism.stl")
