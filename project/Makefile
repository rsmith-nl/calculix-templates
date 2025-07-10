# vim:fileencoding=utf-8:ft=make
.POSIX:
.SUFFIXES:
.PHONY: mesh disp strain stress clean include help 

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
	ccx -i job |2>&1 tee job.log
	@rm -f spooles.out *.12d *.cvg *.sta
	@rm -f *Miss*.nam

# Run the solver for nonlinear analysis
job.frd: job.inp all.msh
	ccx -i job|2>&1 tee job.log | \
		grep -E 'nodes:|   elements:|actual total time|^ iteration|Total CalculiX Time|^ convergence'
	@rm -f spooles.out *.12d *.cvg *.sta
	@rm -f *Miss*.nam

# Post-processor commands
mesh: all.msh ## view the mesh
	cgx -b view-mesh.fbd

disp: job.frd view-disp.fbd ## view displacements
	cgx -b view-disp.fbd

strain: job.frd view-strain.fbd ## view strain
	cgx -b view-strain.fbd

stress: job.frd view-stress.fbd ## view stress
	cgx -b view-stress.fbd

# Housekeeping
clean: ## clean up the working directory
	rm -f *.equ *.sur *.nam *.msh *.log *.12d *.cvg *.sta *.con
	rm -f spooles.out

include: ## generate include statements for solver input file
	@ls *.msh *.nam *.sur *.equ *.con|sed -e 's/^/\*INCLUDE, INPUT=/'

help:
	@echo "Command  Meaning"
	@echo "-------  -------"
	@sed -n -e '/##/s/:.*\#\#/\t/p' -e '/@sed/d' Makefile
