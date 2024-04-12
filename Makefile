# vim:fileencoding=utf-8:fdm=marker:ft=make
.POSIX:
.SUFFIXES:

all: all.msh job.frd

# Run cgx as the pre-processor
all.msh: pre.fbd
	cgx -bg pre.fbd
	cat DCF* ICF* > ties.sur
	rm -f ICF* DCF*

# Run gmsh as the pre-processor
all.msh: waterdeksel.stp pre.geo
	gmsh pre.geo -
	gmsh-inp-filter --log=info gmsh-output.inp all.msh
	rm -f gmsh-output.inp

# Note: to take advantage of multiple cores,
# OMP_NUM_THREADS should be set in the environment.
# Run the solver for linear analysis
job.frd: job.inp all.msh
	@ccx -i job | tee job.log
	@rm -f spooles.out *.12d *.cvg *.sta
	@rm -f *Miss*.nam

# Run the solver for nonlinear analysis
job.frd: job.inp all.msh
	@ccx -i job| tee job.log | grep -E 'nodes:|   elements:|actual total time'
	@rm -f spooles.out *.12d *.cvg *.sta
	@rm -f *Miss*.nam

# Post-processor commands
mesh: all.msh .PHONY ## view the mesh
	cgx -b view-mesh.fbd

disp: job.frd view-disp.fbd .PHONY ## view displacements
	cgx -b view-disp.fbd

strain: job.frd view-strain.fbd .PHONY ## view strain
	cgx -b view-strain.fbd

stress: job.frd view-stress.fbd .PHONY ## view stress
	cgx -b view-stress.fbd

# Housekeeping
clean: .PHONY ## clean up the working directory
	rm -f *.equ *.sur *.nam *.msh *.log *.12d *.cvg *.sta *.con
	rm -f spooles.out

include: .PHONY ## generate include statements for solver input file
	@ls *.msh *.nam *.sur *.equ *.con|sed -e 's/^/\*INCLUDE, INPUT=/'

help: .PHONY
	@echo "Command  Meaning"
	@echo "-------  -------"
	@sed -n -e '/##/s/:.*\#\#/\t/p' -e '/@sed/d' Makefile
