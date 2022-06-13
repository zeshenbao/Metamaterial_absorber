


from cadquery import Vertex
import cadquery as cq
from cadquery import exporters
import argparse
from io import StringIO

result = cq.Workplane("front").rect(1, 1).workplane(offset=2.0).circle(0.001).loft(combine=True)
show_object(result)