<#

.SYNOPSIS

Runs the Calculix preprocessor.

.DESCRIPTION

Calls the CalculiX preprocessor “cgx” to process the input file “pre.fbd”

#>
cgx -bg pre.fbd
Get-Content *CF*.sur | Set-Content ties.sur
Remove-Item -Path "*CF*.sur" -ErrorAction SilentlyContinue
