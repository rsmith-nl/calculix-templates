<#

.SYNOPSIS

Runs the Calculix preprocessor.

.DESCRIPTION

Calls the CalculiX preprocessor “cgx” to process the input file “pre.fbd”

#>
$preprocfile="pre.fbd"
if (!(Test-Path $preprocfile)) {
    Write-Warning "File $preprocfile not found! Exiting."
    exit 1
}
cgx -bg $preprocfile
if (Test-Path *CF*.sur -PathType Leaf) {
    Write-Information -MessageData "Combining DCF and ICF files into ties.sur."
    Get-Content *CF*.sur | Set-Content ties.sur
    Remove-Item -Path "*CF*.sur" -ErrorAction SilentlyContinue
}
