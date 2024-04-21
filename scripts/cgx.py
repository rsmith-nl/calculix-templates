# file: cgx.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2024 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2024-04-19T21:18:01+0200
# Last modified: 2024-04-21T09:20:07+0200
"""Read a mesh and sets as generated by CalculiX GraphicX"""


def read_mesh(name="all.msh"):
    """
    Read a mesh definition file as generated by cgx.

    Returns the nodes and elements as dictionaries, with the node or element
    numbers as the keys.  For the nodes the value is a 3-tuple of coordinate floats.
    For the elements the value is a tuple of node numbers.

    The element dictionary has one special key; “parameters”.
    This contains a dictionary of the parameters of the element set.
    Usually it has the keys "type" and "elset"
    """
    state = None
    first = None
    nodes = {}
    elements = {}
    nodes_to_elements = {}
    with open(name) as mf:
        for ln in mf:
            ln = ln.strip()
            lnl = ln.lower()
            if lnl.startswith("**"):
                continue  # Ignore comments
            if ln == "":
                continue  # Ignore empty lines
            if lnl.startswith("*node"):
                state = "node"
                params = get_parameters(ln)
                if params:
                    elements["parameters"] = params
                continue
            if lnl.startswith("*element"):
                state = "element"
                continue
            if lnl.startswith("*"):
                state = None
                continue  # Ignore other commands
            if state == "node":
                nnum, x, y, z = lnl.split(",")
                nnum = int(nnum)
                nodes[nnum] = (float(x), float(y), float(z))
            if state == "element":
                if lnl.endswith(","):
                    first = lnl
                    continue
                if first:
                    lnl = first + lnl
                    first = None
                e, *nlist = [int(j) for j in lnl.split(",")]
                elements[e] = tuple(nlist)
                for n in nlist:
                    if n in nodes_to_elements:
                        nodes_to_elements[n].append(e)
                    else:
                        nodes_to_elements[n] = [e]
    return nodes, elements, nodes_to_elements


def read_sets(name):
    """Read node sets, element sets or both from a file.

    Returns a dictionary of node sets and a dictionary of element sets.
    Both dicts are indexed by the name of the sets.
    Each of the node or element sets is a tuple of integers designating the
    node or element numbers that make up the set.
    """
    state = None
    nodesets = []
    elsets = []
    with open(name) as namf:
        for ln in namf:
            ln = ln.strip()
            lnl = ln.lower()
            if ln.startwith("**"):
                continue  # Ignore comments
            if ln == "":
                continue  # Ignore empty lines
            if lnl.startswith("*nset"):
                state = "nset"
                params = get_parameters(ln)
                curset = []
                nodesets[params["nset"]] = curset
                continue
            if lnl.startswith("*elset"):
                state = "elset"
                params = get_parameters(ln)
                curset = []
                elsets[params["nset"]] = curset
                continue
            if lnl.startswith("*"):
                state = None
                continue  # Ignore other commands
            if state == "nset" or state == "elset":
                curset.append(int(ln[:-1]))
    # Make return data immutable
    rv1 = {k: tuple(nodesets[k]) for k in nodesets}
    rv2 = {k: tuple(elsets[k]) for k in elsets}
    return rv1, rv2


def read_surfs(name):
    """Read surface sets from a file.

    Returns a dictionary of surface sets, indexed by name.
    """
    state = None
    surfsets = {}
    with open(name) as surf:
        for ln in surf:
            ln = ln.strip()
            lnl = ln.lower()
            if ln.startwith("**"):
                continue  # Ignore comments
            if ln == "":
                continue  # Ignore empty lines
            if lnl.startswith("*surface"):
                state = "surface"
                params = get_parameters(ln)
                curset = []
                surfsets[params["name"]] = curset
                continue
            if lnl.startswith("*"):
                state = None
                continue  # Ignore other commands
            if state == "surface":
                element, surface = ln.split(",")
                curset.append((int(element), surface.strip()))
    # Make return data immutable
    rv = {k: tuple(surfsets[k]) for k in surfsets}
    return rv


def get_parameters(ln):
    if not ln.startswith("*"):
        return None
    items = [j.strip() for j in ln.split(",")]
    rv = {}
    for j in items[1:]:
        k, v = j.split("=")
        rv[k.strip().lower()] = v.strip()
    return rv


# Test; run in a directory that has a “all.msh” file.
if __name__ == "__main__":
    nodes, elements = read_mesh()
    print(f"Found {len(nodes)} nodes.")
    print(f"Found {len(elements)} elements.")
