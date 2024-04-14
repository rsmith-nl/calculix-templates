# file: force.py
# vim:fileencoding=utf-8:ft=python
"""Read and report the forces on requested set and direction"""

import sys

filename = sys.argv[1]
if not filename.endswith(".dat"):
    print("ERROR: input file name must end in '.dat'.", file=sys.stderr)
    sys.exit(1)
setname = sys.argv[2].upper()  # Set names are in upper case in the dat-file.
IX = {
    "x": 1,
    "y": 2,
    "z": 3,
}
try:
    index = IX[sys.argv[3].lower()]
except KeyError:
    print("ERROR: index must be in (x,y,z)", file=sys.stderr)

state = None  # Not reading
force = 0.0
with open("job.dat") as datfile:
    for ln in datfile:
        if "set" in ln:  # Report header
            state = None  # Only some sets are read
            if "forces" in ln and setname in ln:
                state = "read"
            continue
        if state == "read":
            if ln.isspace():
                # skip empty lines
                continue
            items = ln.strip().split()
            force += float(items[index])
print(f"Total force on set “{setname}” = {force:.0f} N")
