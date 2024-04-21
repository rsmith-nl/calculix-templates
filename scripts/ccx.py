# file: ccx.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2024 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2024-04-21T11:14:11+0200
# Last modified: 2024-04-21T15:12:33+0200
"""Read result data from CalculiX .frd files."""


def read_frd(fname="job.frd"):
    """
    Reads results from an .frd file.

    Currently, only the following types are handled:
    * DISP
    * STRESS
    * ZZSTR
    * MESTRAIN
    * FORC
    * ENER
    * PE
    * NDTEMP

    The results are returned as a nested dictionary.
    The first level is the step.
    """
    results = {}
    name = None
    numstep = None
    with open(fname) as frd:
        for ln in frd:
            key = ln[0:5].strip()
            if key == "100":
                # See “Nodal results block” in cgx manual.
                numstep = int(ln[58:63])
                if numstep not in results:
                    results[numstep] = {}
                continue
            if key == "-4":
                name = ln.split()[1]
                results[numstep][name] = {}
                continue
            if key == "-3":
                name = None
                numstep = None
                continue
            if key == "9999":
                return results
            if key == "-1":
                if name in ("DISP", "FORC"):
                    node = int(ln[3:13])
                    x = float(ln[13:25])
                    y = float(ln[25:37])
                    z = float(ln[37:49])
                    results[numstep][name][node] = (x, y, z)
                    continue
                if name in ("STRESS", "ZZSTR", "MESTRAIN"):
                    node = int(ln[3:13])
                    xx = float(ln[13:25])
                    yy = float(ln[25:37])
                    zz = float(ln[37:49])
                    xy = float(ln[49:61])
                    yz = float(ln[61:73])
                    zx = float(ln[73:85])
                    results[numstep][name][node] = (xx, yy, zz, xy, yz, zx)
                    continue
                if name in ("ERROR", "ENER", "PE", "NDTEMP"):
                    node = int(ln[3:13])
                    data = float(ln[13:25])
                    results[numstep][name][node] = data
