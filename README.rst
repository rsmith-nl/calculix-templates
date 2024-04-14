Templates for use with CalculiX
###############################

:date: 2024-04-14
:tags: CalculiX, templates
:author: Roland Smith

.. Last modified: 2024-04-14T22:57:20+0200
.. vim:spelllang=en

This repository contains snippets of pre- and post processor or solver code
that I have developed over the years. All the files are plain text. They can
be opened with any editor.

For understanding the contents it is *highly* recommended to have the
manuals for the preprocessor and solver at hand when reading these files.

Note that these file are not intended as an introduction to CalculiX for newbies.
If you are new to CalculiX you might want to try out the FEA workbench in FreeCAD_.
If you mainly work with isotropic materials, this is a decent way to do FEA.

.. _FreeCAD: https://www.freecad.org/

A short introduction of the different subdirectories.


Geometry
--------

One of the functions of the CalculiX preprocessor ``cgx`` is to generate
geometries that can be meshed by the built-in mesher.
This directory contains several preprocessor command files as examples of that.
Preprocessor command files have the ``fbd`` extension.

It combines both the generation of geometry and meshes and those are strongly
coupled.
So it is not a general purpose CAD program. But with some forethought it can
be used to generate good regular hexahedron meshes.


Materials
---------

In this directory several files defining materials in the CalculiX solver
``inp`` format can be found.
The names speak for themselves.
All the material properties are based on publicly available data.

Note that for materials where ``*PLASTIC`` data is supplied, you might want to
comment those out initially to do a linear analysis.


Postprocessing
--------------

This shows some ways how to extract images and numbers from the results of
a solver run.


Project
-------

Probably the most important subdirectory.

This contains all the files needed to create an analysis in CalculiX.

* ``pre.fbd`` -- to create the geometry and mesh
* ``job.inp`` -- instructs the solver what to do.
* ``view-*``  -- are different viewers for the result
* ``Makefile`` -- A command file for the ``make(1)`` program.

For a new analysis, I generally start by making a copy of the contents of this
directory.
Then I take one of more of the ``*STEP`` cards defined in the ``steps``
directory and add them to the input file.

On current UNIX-like systems ``make`` is generally available out-of-the-box.

The ``Makefile`` ties everything together.
It describes which commands are to be run to e.g. create the mesh, run the
solver or display the results.
Note that the ``Makefile`` should be edited before use!
It contains two different workflows for creating the mesh; one based on using
the ``cgx`` preprocessor, and one using the ``gmsh`` mesh generator and
a STEP file for the geometry.
There are also two solver workflows; for a linear and nonlinear analysis.

If any of the above files have changed since the
analysis was run, using ``make`` will re-run the needed steps.
Running ``make help`` will show which sub-commands are available


Scripts
-------

A couple of scripts that show how to read meshes or results using Python 3.


Steps
-----

Steps are basically the last pieces of the solver input file.
They describe which analysis to use, what loads to apply and which results to
save.

The name of the files should speak for themselves.

Where useful both linear and nonlinear analysis are shown.
