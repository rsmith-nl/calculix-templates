# file: read-mesh.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2023 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2023-10-20T10:34:06+0200
# Last modified: 2023-10-20T10:54:09+0200
"""Read “all.msh” into Python"""

import logging
import sys

logging.basicConfig(
    level="INFO",
    format="%(levelname)s: %(message)s",
)

with open("all.msh") as mf:
    lines = [ln.strip() for ln in mf]
    logging.info(f"read {len(lines)} lines")

nset = [n for n, ln in enumerate(lines) if "*NODE" in ln]
logging.info(f"found {len(nset)} node sets")
if len(nset) != 1:
    logging.error("more than one node set")
    sys.exit(1)
nset = nset[0]

elset = [n for n, ln in enumerate(lines) if "*ELEMENT" in ln]
logging.info(f"found {len(elset)} element sets")
if len(elset) != 1:
    logging.error("more than one element set")
    sys.exit(2)
elset = elset[0]
if "C3D20" not in lines[elset]:
    logging.error("not C3D20(R) elements")
    sys.exit(3)

nodegen = (ln.split(",") for ln in lines[nset + 1 : elset])
nodes = {int(n): (float(x), float(y), float(z)) for n, x, y, z in nodegen}
logging.info(f"read {len(nodes)} nodes")

if "C3D20" in lines[elset]:
    combinegen = (
        (a + b).split(",") for a, b in zip(lines[elset + 1 :: 2], lines[elset + 2 :: 2])
    )
    elements = {int(items[0]): tuple(int(j) for j in items[1:]) for items in combinegen}
    logging.info(f"read {len(elements)} C3D20(R) elements")
