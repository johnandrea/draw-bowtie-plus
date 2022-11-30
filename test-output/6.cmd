@echo off

set in="..\test-data\small-royals-2022.ged"
set prog="..\draw-bowtie-plus.py"
set n="6"

if exist %n%.dot del %n%.dot
if exist %n%.err del %n%.err
if exist %n%.png del %n%.png
if exist tree.err del tree.err

rem King Charles bowtie
%prog% --title="Charles branch" --orient=lr %in% 9 >%n%.dot 2>%n%.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng %n%.dot -o %n%.png 2>tree.err
