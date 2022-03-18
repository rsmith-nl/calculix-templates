
# vim:fileencoding=utf-8:fdm=marker:ft=make
.PHONY: mesh disp stress core clean include

all: all.msh job.frd

# Run the pre-processor
all.msh: pre.fbd
	cgx -bg pre.fbd
	cat DCF* ICF* > ties.sur
	rm -f ICF* DCF*

# Run the solver
job.frd: job.inp all.msh
	env OMP_NUM_THREADS=4 ccx -i job
	rm -f job.log spooles.out *.12d *.cvg *.sta
	rm -f *Miss*.nam

# Different post-processor commands

# view the mesh
mesh: all.msh
	cgx -b view-mesh.fbd

# view displacements
disp: job.frd view-disp.fbd
	cgx -b view-disp.fbd

# view strain
strain: job.frd view-strain.fbd
	cgx -b view-strain.fbd

# view stress
stress: job.frd view-stress.fbd
	cgx -b view-stress.fbd

# Helpers
clean::
	rm -f *.equ *.sur *.nam *.msh *.log spooles.out *.12d *.cvg *.sta *.con

include::
	@ls *.msh *.nam *.sur *.equ *.con|sed -e 's/^/\*INCLUDE, INPUT=/'
