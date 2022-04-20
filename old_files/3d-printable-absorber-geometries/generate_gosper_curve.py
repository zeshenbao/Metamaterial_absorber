#!/usr/bin/env python2

"""
Generate Gosper 37a-1 curve absorber geometries
CadQuery 1.2.0
FreeCAD 0.17

This script is Python 2 due to Python 3 compatibility issues encountered with
CadQuery when the script was written.

Matthew Petroff, 2017-2018
"""

__author__ = "Matthew Petroff"

import argparse
import StringIO
import numpy as np
import cadquery as cq

parser = argparse.ArgumentParser(
    description="Generate Gosper 37a-1 curve absorber geometry."
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
args = parser.parse_args()


# Wedge height
height = args.height
# Segment thickness
thickness = args.thickness
# Segment length
length = thickness / np.sin(np.deg2rad(60))
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
    .extrude(thickness)
    .translate((-thickness / 2, 0, 0))
)
intersection_b = intersection_a.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 240)
intersection = intersection_a.findSolid().intersect(intersection_b.findSolid())
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
union_b = union_a.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 240)
corner = cq.CQ(union_a.union(union_b).union(intersection).findSolid())

# Tight corner primitive
corner_b = corner.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 60)
intersection = corner.findSolid().intersect(corner_b.findSolid())
corner2 = cq.CQ(intersection)

# Side primitive
side = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(length)
)

# End cap
end_cap = (
    cq.Workplane("YZ")
    .lineTo(-thickness / 2, 0)
    .lineTo(-thickness / 2, base_thickness)
    .lineTo(0, height + base_thickness)
    .lineTo(thickness / 2, base_thickness)
    .lineTo(thickness / 2, 0)
    .close()
    .extrude(thickness / 2)
)


# L-system definition
axiom = "A"
A = "AFAFA+BFBFBF+FAFA+BFBFBF+FA+BFBF+FA+BF++BF-FA--FAFA-BF-FAFA-BFBF-FAFAFA-BFBF-FAFAFAFA-BFBFBF+"
B = "-FAFAFA+BFBFBFBF+FAFA+BFBFBF+FAFA+BFBF+FA+BFBF++BF+FA--FA-BF-FAFA-BF-FAFAFA-BFBF-FAFAFA-BFBFB"

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
while "++" in lsystem:
    lsystem = lsystem.replace("++", "P")
while "--" in lsystem:
    lsystem = lsystem.replace("--", "M")


# Start cap
result = side.translate((-thickness / 2, 0.0, 0.0))

# L-system iteration variables
angle = 0
x = 0
y = 0

# Iterate through L-system
for i, sym in enumerate(lsystem):
    if sym == "-":
        angle = (angle - 60) % 360
        result = result.add(
            corner.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle + 180).translate(
                (x, y, 0.0)
            )
        )
    elif sym == "+":
        angle = (angle + 60) % 360
        result = result.add(
            corner.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle - 90 + 30).translate(
                (x, y, 0.0)
            )
        )
    elif sym == "M":
        angle = (angle - 120) % 360
        result = result.add(
            corner2.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle + 180).translate(
                (x, y, 0.0)
            )
        )
    elif sym == "P":
        angle = (angle + 120) % 360
        result = result.add(
            corner2.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle - 90 - 30).translate(
                (x, y, 0.0)
            )
        )
    elif sym == "F":
        result = result.add(
            side.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), angle)
            .translate((x, y, 0.0))
            .findSolid()
        )
        x += length * np.cos(np.deg2rad(angle))
        y += length * np.sin(np.deg2rad(angle))

result = result.union(result)


# Save result and edit metadata
output = StringIO.StringIO()
cq.exporters.exportShape(result, "STEP", output)
step_data = output.getvalue()
output.close()
description = step_data.split("FILE_DESCRIPTION", 1)
step_data = (
    description[0]
    + "FILE_DESCRIPTION(('Gosper curve 37a-1 "
    + "absorber geometry, order {}'),".format(iterations)
    + description[1].split(",", 1)[1]
)
name = step_data.split("FILE_NAME", 1)
name_items = name[1].split(";", 1)[0].split(",")
step_data = (
    name[0]
    + ",".join(
        [
            "FILE_NAME('gosper37a-1_{}'".format(iterations),
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
with open("gosper37a-1_{}.step".format(iterations), "w") as f:
    f.write(step_data)
