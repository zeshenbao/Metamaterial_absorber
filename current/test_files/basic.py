import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO


box = cq.Workplane("XY").box(3.0,2.0,0.5)

exporters.export(box, "debugg4.stl")
