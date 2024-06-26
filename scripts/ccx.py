# file: ccx.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2024 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2024-04-21T11:14:11+0200
# Last modified: 2024-05-28T21:34:45+0200
"""Read result data from CalculiX .frd and .dat files."""

_NODE_RELATED = (
    "CONTACT",
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
    "NODES",
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
    fmt = None
    with open(fname) as frd:
        for ln in frd:
            key = ln[0:5].strip()
            if key == "100":
                # See “Nodal results block” in cgx manual.
                numstep = int(ln[58:63])
                fmt = int(ln[73:75])
                if fmt > 1:
                    raise ValueError(f"fmt={fmt}; binary data not handled")
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
                    if fmt == 1:
                        node = int(ln[3:13])
                    elif fmt == 0:
                        node = int(ln[3:8])
                    rv = tuple(_floats(ln, fmt))
                    if len(rv) == 1:
                        rv = rv[0]
                    results[numstep][name][node] = rv
                    continue


def read_dat(fname="job.dat"):
    """Reads results from a .dat file.

    The results are returned as a list.
    Each item is a dictionary of:
    * name of the result in question
    * keys: a tuple that names each of the data items.
    * setname: the name of the set the data belongs to.
    * data: a dict of n-tuples indexed by node or element number containing actual values.
        If n = 1, the tuple is replaced by its single value
    """
    results = []
    current = None
    with open(fname) as dat:
        for ln in dat:
            if "for set" in ln:
                name, keys, setname, time = _find_result(ln)
                current = {
                    "name": name,
                    "keys": keys,
                    "setname": setname,
                    "time": time,
                    "data": {},
                }
                results.append(current)
                continue
            if not ln or ln.isspace():
                continue  # skip empty lines
            if current:
                try:
                    floats = [float(j) for j in ln.split()]
                    if floats[0].is_integer():  # node or element number
                        num = int(floats[0])
                        if "integ.pnt." in current["keys"]:
                            ip = int(floats[1])
                            if num not in current["data"]:
                                current["data"][num] = {ip: _unwrap_or_tuple(floats[2:])}
                            else:
                                current["data"][num][ip] = _unwrap_or_tuple(floats[2:])
                        else:
                            current["data"][num] = _unwrap_or_tuple(floats[1:])
                    else:
                        current["data"] = _unwrap_or_tuple(floats)
                except ValueError:
                    current = None
    return results


def _unwrap_or_tuple(data):
    """Unwrap data if length is 1, else convert into tuple."""
    if len(data) == 1:
        return data[0]
    return tuple(data)


def _floats(ln, fmt=0):
    length = 12
    if fmt == 1:
        start = 13
    elif fmt == 0:
        start = 8
    stop = start + length
    while start < len(ln):
        try:
            yield float(ln[start:stop])
        except ValueError:
            pass
        start += length
        stop += length


def _find_result(line):
    """Extracts the data type name, keys (if any), set name and time."""
    first, _, last = line.partition("for set")
    first = first.strip()
    if first.endswith(")"):  # we have keys...
        name, _, items = first[:-1].partition("(")
        items = [j.strip() for j in items.split(",")]
        if "elem" not in items[0] and not (
            "mass" in name or "center of gravity" in name
        ):  # node based
            items.insert(0, "node")
    else:  # the name is also the only key
        name = first
        items = [first]
    setname, _, time = last.partition("and time")
    return (name.strip(), tuple(items), setname.strip(), float(time))
