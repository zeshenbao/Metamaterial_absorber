

import cadquery as cq
from cadquery import exporters
from math import *

#drill a hole in the side
c = cq.Workplane().box(1,1,1).faces(">Z").workplane().circle(0.25).cutThruAll()

# now cut it in half sideways
c = c.faces(">Y").workplane(-0.3).split(keepTop=True)

exporters.export(c, "c.stl")
