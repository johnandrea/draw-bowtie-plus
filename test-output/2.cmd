@echo off

set in="..\test-data\skywalker-movies.ged"
set prog="..\draw-bowtie-plus.py"

rem Padme's ancestors and descendents. Back one generation to show sister.
%prog% --title="Padme branch + siblings" --from=1 --desc=100 --orient=lr %in% 4 >2.dot 2>run.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng 2.dot -o 2.png 2>tree.err
