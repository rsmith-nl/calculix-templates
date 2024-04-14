# file: read-surface-set.py
# vim:fileencoding=utf-8:ft=python
"""Read a CalculiX surface set"""

import logging
import sys

logging.basicConfig(
    level="INFO",
    format="%(levelname)s: %(message)s",
)

if len(sys.argv) < 2:
    logging.error("supplying a surface set name is required")
    sys.exit(1)


with open(sys.argv[1]) as sf:
    lines = [ln.strip() for ln in sf]
    logging.info(f"read {len(lines)} lines")

surfstarts = [n for n, ln in enumerate(lines) if '*SURFACE,' in ln]
logging.info(f"{len(surfstarts)} surface sets found")

endlines = surfstarts[1:] + [len(lines)+1]
surfaces = {}
for first, end in zip(surfstarts, endlines):
    line = lines[first]
    name = line[line.index("NAME=")+5:]
    surfaces[name] = {}
    data = lines[first+1:end]
    for ln in data:
        # Ignore comments.
        if "**" in ln:
            continue
        num, face = ln.split(",")
        num = int(num)
        face = int(face[2])
        surfaces[name][num] = face
    logging.info(f"surface “{name}” has {len(surfaces[name])} facets")
