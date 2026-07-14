<#

.SYNOPSIS

Runs the Calculix postprocessor.

.DESCRIPTION

Calls the CalculiX postprocessor “cgx” to process the file view-<argument>.fbd

PARAMETER argument
        Specifies part of the filename after “view-”.

#>
$argument=$args[0]
$target="view-$argument.fbd"
if (Test-Path $target -PathType Leaf) {
    cgx -b $target
} else {
    Write-Warning "File $target not found! Exiting."
    exit 1
}
