# file: rect-with-hole.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2023 R.F. Smith <rsmith@xs4all.nl>
# Created: 2023-10-08T08:56:41+0200
# Last modified: 2023-10-08T13:28:14+0200
"""Script to generate the CGX geometry for a rectangle with a hole."""

import argparse
import logging
import math
import sys

__version__ = "2023.10.08"


formats = {
    "XY": ("pnt p{0} {1:.6f} {2:.6f} {3:.6f}", "pnt cp {0:.6f} {1:.6f} {2:.6f}"),
    "XZ": ("pnt p{0} {1:.6f} {3:.6f} {2:.6f}", "pnt cp {0:.6f} {2:.6f} {1:.6f}"),
    "YZ": ("pnt p{0} {3:.6f} {1:.6f} {2:.6f}", "pnt cp {2:.6f} {0:.6f} {1:.6f}"),
}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-v", "--version", action="version", version=__version__)
parser.add_argument(
    "--log",
    default="warning",
    choices=["debug", "info", "warning", "error"],
    help="logging level (defaults to 'warning')",
)
parser.add_argument(
    "-p",
    "--plane",
    default="XY",
    choices=["XY", "XZ", "YZ"],
    help="plane for the geometry to sit in (defaults to XY)",
)
parser.add_argument(
    "--poff",
    default=0.0,
    type=float,
    help="offset from the plane (defaults to 0)",
)
parser.add_argument(
    "--hoff",
    default=0.0,
    type=float,
    help="horizontal offset of the hole in the rectangle (defaults to 1/2 the width)",
)
parser.add_argument(
    "--voff",
    default=0.0,
    type=float,
    help="vertical offset of the hole in the rectangle (defaults to 1/2 the height)",
)
parser.add_argument(
    "--width",
    default=30.0 / 1000,
    type=float,
    help="rectangle width (defaults to 0.030)",
)
parser.add_argument(
    "--height",
    default=20.0 / 1000,
    type=float,
    help="rectangle height (defaults to 0.020)",
)
parser.add_argument(
    "--dia",
    default=6.0 / 1000,
    type=float,
    help="hole diameter (defaults to 0.006)",
)
parser.add_argument(
    "--div",
    default=8,
    type=int,
    help="line divisions (defaults to 8)",
)

args = parser.parse_args(sys.argv[1:])
# Configure logging
logging.basicConfig(
    level=getattr(logging, args.log.upper(), None),
    format="%(levelname)s: %(message)s",
)
args.plane = args.plane.upper()

print(f"# Generated by {sys.argv[0]}")
print("# with arguments:", *sys.argv[1:])

if args.hoff == 0:
    args.hoff = args.width / 2
if args.voff == 0:
    args.voff = args.height / 2

p1 = (0, 0)
p2 = (args.width, 0)
p3 = (args.width, args.height)
p4 = (0, args.height)
cp = (args.hoff, args.voff)

divl = args.div

d1 = (cp[0] - p1[0], cp[1] - p1[1])
l1 = math.sqrt(d1[0] ** 2 + d1[1] ** 2)
l1 = (l1 - args.dia / 2) / l1
p5 = (p1[0] + l1 * d1[0], p1[1] + l1 * d1[1])

d2 = (cp[0] - p2[0], cp[1] - p2[1])
l2 = math.sqrt(d2[0] ** 2 + d2[1] ** 2)
l2 = (l2 - args.dia / 2) / l2
p6 = (p2[0] + l2 * d2[0], p2[1] + l2 * d2[1])

d3 = (cp[0] - p3[0], cp[1] - p3[1])
l3 = math.sqrt(d3[0] ** 2 + d3[1] ** 2)
l3 = (l3 - args.dia / 2) / l3
p7 = (p3[0] + l3 * d3[0], p3[1] + l3 * d3[1])

d4 = (cp[0] - p4[0], cp[1] - p4[1])
l4 = math.sqrt(d4[0] ** 2 + d4[1] ** 2)
l4 = (l4 - args.dia / 2) / l4
p8 = (p4[0] + l4 * d4[0], p4[1] + l4 * d4[1])

for n, (x, y) in enumerate((p1, p2, p3, p4, p5, p6, p7, p8), start=1):
    print(formats[args.plane][0].format(n, x, y, args.poff))
print(formats[args.plane][1].format(cp[0], cp[1], args.poff))

for j in range(1, 4):
    print(f"line l{j} p{j} p{j+4} {divl}")
    print(f"line l{j+4} p{j} p{j+1} {divl}")
    print(f"line l{j+8} p{j+4} p{j+5} cp {divl}")
print(f"line l4 p4 p8 {divl}")
print(f"line l8 p4 p1 {divl}")
print(f"line l12 p8 p5 cp {divl}")
print("surf s1 blend l1 l9 l2 l5")
print("surf s2 blend l2 l10 l3 l6")
print("surf s3 blend l3 l11 l4 l7")
print("surf s4 blend l4 l12 l8 l1")

print("plot pa all")
print("plus la all")
print("plus sa all")
