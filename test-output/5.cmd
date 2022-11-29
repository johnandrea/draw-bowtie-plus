@echo off

set in="..\test-data\skywalker-movies.ged"
set prog="..\draw-bowtie-plus.py"

rem Leia's cousins. Back two generations down two generations.
%prog% --title="Leia aunts,uncles,cousins" --anc=2 --from=2 --desc=2 --orient=lr %in% 6 >5.dot 2>run.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng 5.dot -o 5.png 2>tree.err
