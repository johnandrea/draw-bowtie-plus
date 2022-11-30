@echo off

set in="..\test-data\small-royals-2022b.ged"
set prog="..\draw-bowtie-plus.py"
set n="7"

if exist %n%.dot del %n%.dot
if exist %n%.err del %n%.err
if exist %n%.png del %n%.png
if exist tree.err del tree.err

rem Prince William bowtie
%prog% --title="William branch" --orient=lr %in% 17 >%n%.dot 2>%n%.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng %n%.dot -o %n%.png 2>tree.err
