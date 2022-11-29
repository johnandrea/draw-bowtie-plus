@echo off

set in="..\test-data\skywalker-movies.ged"
set prog="..\draw-bowtie-plus.py"

rem Leia's descendents
%prog% --title="Leia descendants" --anc=0 --from=0 --desc=100 --orient=lr %in% 6 >4.dot 2>run.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng 4.dot -o 4.png 2>tree.err
