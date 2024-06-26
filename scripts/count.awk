# file: count.awk
# vim:fileencoding=utf-8:ft=awk
#
# Counts nodes and elements in “all.msh” files.
#
# Copyright © 2024 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2024-04-23T11:28:22+0200
# Last modified: 2024-05-03T19:50:45+0200
BEGIN {nodes=0; elements=0; type=""}
 # Skip comments
/^[[:space:]]*\*\*/ {next;}
# Handle types we want to count.
/^[[:space:]]*\*NODE/ {type = "n"; next}
/^[[:space:]]*\*ELEMENT/ {type = "e"; next}
 # Ignore other commands
/^[[:space:]]*\*/ {type = ""; next}
# Count.
/[^,]$/ {if (type == "n") {nodes += 1} else if (type == "e") {elements += 1}}
END {
printf "* nodes: %d\n", nodes;
printf "* elements: %d\n", elements
}
