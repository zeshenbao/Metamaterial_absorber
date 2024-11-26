from cadquery import Vertex
import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO


original = cq.Workplane("XY").polygon(5, 10).extrude(0.1).translate((1, 1, 2))

#print(type(original))

arc = (
    cq.Workplane()
    .polygon(5, 10)
    .offset2D(1, "arc")
    .extrude(0.1)
    .translate((0, 0, 1))
)
intersection = cq.Workplane().polygon(5, 10).offset2D(1, "intersection").extrude(0.1)
result = original.add(arc).add(intersection)



exporters.export(result, "translate_test.stl")
