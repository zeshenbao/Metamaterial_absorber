#!/usr/bin/env python2

"""
Generate Hilbert curve absorber geometries
CadQuery 1.2.0
FreeCAD 0.17

This script is Python 2 due to Python 3 compatibility issues encountered with
CadQuery when the script was written.

Matthew Petroff, 2017-2018
"""

__author__ = "Matthew Petroff"

import argparse
from io import StringIO
#######################
#import sys

#sys.path.append("D:/Documents/SU/Internship in Physics/3d-printable-absorber-geometries/FreeCAD 0.19/bin")
##################################
import cadquery as cq

parser = argparse.ArgumentParser(
    description="Generate Hilbert curve absorber geometry."
)
parser.add_argument(
    "iterations", metavar="ITER", type=int, help="order / number of L-system iterations"
)
parser.add_argument(
    "--height",
    metavar="H",
    type=float,
    default=1.0,
    help="wedge height (without base) [default 1.0]",
)
parser.add_argument(
    "--thickness",
    metavar="T",
    type=float,
    default=1.0,
    help="segment length / thickness [default 1.0]",
)
parser.add_argument(
    "--base_thickness",
    metavar="H",
    type=float,
    default=1.0,
    help="base thickness [default 1.0]",
)
parser.add_argument(
    "--use_square_ends",
    action="store_const",
    const=True,
    default=False,
    help="Use square ends instead of tapered ends.",
)
args = parser.parse_args()


# Wedge height
height = args.height
# Segment length / thickness
thickness = args.thickness
# Base thickness
base_thickness = args.base_thickness
# L-system iterations
iterations = args.iterations


# Corner primitive
intersection_a = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2, both=True)
)
intersection_b = (
    cq.Workplane("XZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2, both=True)
)
intersection = intersection_a.findSolid().intersect(intersection_b.findSolid())
#print(type(intersection)) #######################################################################
union_a = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(-thickness / 2)
)
union_b = (
    cq.Workplane("XZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(-thickness / 2)
)
corner = cq.CQ(union_a.union(union_b).union(intersection).findSolid())
print(type(corner))
# Side primitive
side = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness)
)
print(type(side))
side_short = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2)
)

# End cap
end_cap = (
    side.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 90)
    .intersect(side.translate((-thickness / 2, 0.0, 0.0)))
    .rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), -90)
)


# L-system definition
axiom = "A"
A = "-BF+AFA+FB-"
B = "+AF-BFB-FA+"


# Prepare L-system
lsystem = axiom
for _ in range(iterations):
    lsystem = (
        lsystem.replace("A", "a").replace("B", "b").replace("a", A).replace("b", B)
    )
lsystem = lsystem.replace("A", "").replace("B", "")
while "+-" in lsystem:
    lsystem = lsystem.replace("+-", "")
while "-+" in lsystem:
    lsystem = lsystem.replace("-+", "")
lsystem = lsystem.strip("+-")


# Start cap
if args.use_square_ends:
    result = side.translate((-thickness / 2, 0.0, 0.0))
    print(type(result))
else:
    result = end_cap.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 180)
    print(type(result))
# L-system iteration variables
angle = 0
x = 0
y = 0

# Iterate through L-system
for i, sym in enumerate(lsystem):
    if sym == "-":
        angle = (angle - 90) % 360
        result = result.add(
            corner.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle + 180).translate(
                (x, y, 0.0)
            )
        )
    elif sym == "+":
        angle = (angle + 90) % 360
        result = result.add(
            corner.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle - 90).translate(
                (x, y, 0.0)
            )
        )
        print(type(result))###########################################################
    elif sym == "F":
        if (
            i < len(lsystem) - 2
            and lsystem[i + 1] in "+-"
            and i > 0
            and lsystem[i - 1] in "+-"
        ):
            pass
        elif i < len(lsystem) - 2 and lsystem[i + 1] in "+-":
            result = result.add(
                side_short.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle).translate(
                    (x, y, 0.0)
                )
            )
        elif i > 0 and lsystem[i - 1] in "+-":
            result = result.add(
                side_short.translate((thickness / 2, 0.0, 0.0))
                .rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle)
                .translate((x, y, 0.0))
            )
        else:
            result = result.add(
                side.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle).translate(
                    (x, y, 0.0)
                )
            )
        if angle == 0:
            x += thickness
        elif angle == 90:
            y += thickness
        elif angle == 180:
            x -= thickness
        elif angle == 270:
            y -= thickness

# Add end cap
if args.use_square_ends:
    result = result.add(
        side_short.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle).translate(
            (x, y, 0.0)
        )
    )
else:
    result = result.add(
        end_cap.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle).translate((x, y, 0.0))
    )
result = result.union(result)


# Save result and edit metadata
output = StringIO()
cq.exporters.exportShape(result, "STEP", output)
step_data = output.getvalue()
output.close()
description = step_data.split("FILE_DESCRIPTION", 1)
step_data = (
    description[0]
    + "FILE_DESCRIPTION(('Hilbert curve absorber "
    + "geometry, order {}'),".format(iterations)
    + description[1].split(",", 1)[1]
)
name = step_data.split("FILE_NAME", 1)
name_items = name[1].split(";", 1)[0].split(",")
step_data = (
    name[0]
    + ",".join(
        [
            "FILE_NAME('hilbert_MOD{}'".format(iterations),
            "''",
            "('{}')".format(__author__),
            "('')",
            name_items[4].strip(),
            name_items[5].strip(),
            "'');",
        ]
    )
    + name[1].split(";", 1)[1]
)
with open("hilbert_MOD{}.step".format(iterations), "w") as f:
    f.write(step_data)
