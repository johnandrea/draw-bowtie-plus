@echo off

set in="..\test-data\skywalker-movies.ged"
set prog="..\draw-bowtie-plus.py"

rem Leia's ancestors.
%prog% --title="Leia ancestors" --desc=0 --down=0 --orient=lr %in% 6 >3.dot 2>3.err

"c:\Program files\Graphviz\bin\dot.exe" -Tpng 3.dot -o 3.png 2>tree.err
