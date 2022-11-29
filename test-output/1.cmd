@echo off

set in="..\test-data\skywalker-movies.ged"
set prog="..\draw-bowtie-plus.py"

rem Padme's ancestors and descendents.
%prog% --title="Padme branch" --from=0 --desc=100 --orient=lr %in% 4 >1.dot 2>run.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng 1.dot -o 1.png 2>tree.err
