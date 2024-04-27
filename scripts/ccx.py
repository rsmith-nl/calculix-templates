# file: ccx.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2024 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2024-04-21T11:14:11+0200
# Last modified: 2024-04-27T15:53:45+0200
"""Read result data from CalculiX .frd files."""

_NODE_RELATED = (
    "NODES",
    "CP3DF",
    "CT3D-MIS",
    "CURR",
    "DEPTH",
    "DISP",
    "DTIMF",
    "ELPOT",
    "EMFB",
    "EMFE",
    "ENER",
    "ERROR",
    "FLUX",
    "FORC",
    "HCRIT",
    "M3DF",
    "MAFLOW",
    "MDISP",
    "MESTRAIN",
    "MSTRAIN",
    "MSTRESS",
    "NDTEMP",
    "PDISP",
    "PE",
    "PFORC",
    "PNDTEMP",
    "PS3DF",
    "PSTRESS",
    "PT3DF",
    "RFL",
    "SDV",
    "SEN",
    "STPRES",
    "STRESS",
    "STRMID",
    "STRNEG",
    "STRPOS",
    "STTEMP",
    "THSTRAIN",
    "TOPRES",
    "TOSTRAIN",
    "TOTEMP",
    "TS3DF",
    "TT3DF",
    "TURB3DF",
    "V3DF",
    "VELO",
    "VSTRES",
    "ZZSTR",
)


def read_frd(fname="job.frd"):
    """
    Reads results from an .frd file.

    Handles all node-related data.

    The results are returned as a nested dictionary.
    The first level is keyed by the step, the second level by the name and the
    last level by the node or element.
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
                if name in _NODE_RELATED:
                    node = int(ln[3:13])
                    results[numstep][name][node] = tuple(_floats(ln))
                    continue


def _floats(ln):
    length = 12
    start = 13
    stop = start + length
    while start < len(ln):
        try:
            yield float(ln[start:stop])
        except ValueError:
            pass
        start += length
        stop += length
