from cadquery import Vertex
import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO


def pyramid(base=(1,1), height=1):
    return (cq.Workplane("XY").rect(base[0], base[1]).workplane(offset=height).circle(0.001).loft(combine=True))

#exporters.export(pyramid((2,2),1), "pyra_XY.stl")
