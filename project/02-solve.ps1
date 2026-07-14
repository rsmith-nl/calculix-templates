<#

.SYNOPSIS

Runs the CalculiX solver ccx.

.DESCRIPTION

Runs the CalculiX solver on the input file “job.inp”.
Afterwards it cleans out some temporary files.

The result data can be found in “job.frd” and “job.dat”.

#>
$solverfile="job.inp"
if (!(Test-Path $solverfile -PathType Leaf)) {
    Write-Warning "File $solverfile not found! Exiting."
    exit 1
}
# Run the solver, copy output to “job.log”.
ccx -i job | Tee-Object -FilePath "job.log"
# Clean up.
Remove-Item -Path "*.12d" -ErrorAction SilentlyContinue
Remove-Item -Path "*.sta" -ErrorAction SilentlyContinue
Remove-Item -Path "*.cvg" -ErrorAction SilentlyContinue
Remove-Item -Path "*Miss*.nam" -ErrorAction SilentlyContinue
Remove-Item -Path "spooles.out" -ErrorAction SilentlyContinue
