import cadquery as cq
from cadquery import exporters


from wall_geometries_class import Geometry

block = Geometry()
block.make_block()
block.add_foundation()


wall = block
corner = block
