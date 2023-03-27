
# vim:fileencoding=utf-8:fdm=marker:ft=make
.PHONY: mesh disp stress core clean include help

all: all.msh job.frd

# Run the pre-processor
all.msh: pre.fbd
	cgx -bg pre.fbd
	cat DCF* ICF* > ties.sur
	rm -f ICF* DCF*

# Run the solver
# Note: to take advantage of multiple cores,
# OMP_NUM_THREADS should be set in the environment.
job.frd: job.inp all.msh
	ccx -i job
	rm -f job.log spooles.out *.12d *.cvg *.sta
	rm -f *Miss*.nam

# Different post-processor commands

mesh: all.msh ## view the mesh
	cgx -b view-mesh.fbd

disp: job.frd view-disp.fbd ## view displacements
	cgx -b view-disp.fbd

strain: job.frd view-strain.fbd ## view strain
	cgx -b view-strain.fbd

stress: job.frd view-stress.fbd ## view stress
	cgx -b view-stress.fbd

clean: ## clean up the working directory
	rm -f *.equ *.sur *.nam *.msh *.log *.12d *.cvg *.sta *.con
	rm -f spooles.out

include: ## generate include statements for solver input file
	@ls *.msh *.nam *.sur *.equ *.con|sed -e 's/^/\*INCLUDE, INPUT=/'

help:
	@echo "Command  Meaning"
	@echo "-------  -------"
	@sed -n -e '/##/s/:.*\#\#/\t/p' -e '/@sed/d' Makefile
