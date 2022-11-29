# draw-bowtie-plus
Genealogical bowtie chart with more options for descendents.

## Installation ##

- Requires python 3.6+
- Copy draw-bowtie-plus.py
- also requires gedcom library [readgedcom.py](https://github.com/johnandrea/readgedcom)
- Output makes use of Graphviz DOT format: [Graphviz](https://graphviz.org)

Or use the .exe file on MS-Windows which is a standalone program in that it doesn't need python or any other the other downloadables.

## Usage ##

Run the program with:
```
diff.py  family.ged  personxref >chart.dot 2>chart.err
```
where personxref is the gedcom id of the person in the middle of the bowtie.
Then convert the .dot file into a displayable file with one (or more) of:
```
graphviz -Tpng chart.dot -o chart.png
graphviz -Tsvg chart.dot -o chart.svg
graphviz -Tpdf chart.dot -o chart.pdf
```
See the Graphviz website for a complete list of [formats](https://graphviz.org/docs/outputs/)

## Options ##

--title="value"

Display a title on the output chart.

--iditem=value

Specify the item to identify the tester via each tester id. Default is "xref" which is the individual
XREF value in the GEDCOM file.
Other options might be "uuid", "refn", etc. If using a GEDCOM custom event specify it as "even dot" followed by
the event name, i.e. "even.extid", "even.myreference", etc.

--ancestors=n

Number of ancestor generations to produce. Default is 100

--descendents=n

Number of descendent generations to produce. Default is 2

--from=n

Number of generations back from the start person to start the descendants. Default is 2 (i.e. grandparents)

--dates

Include birth and death dates with names.

--reverse-arrows

Reverse the order of the arrows between parents and children.

--orientation=direction

Set the orientatation of the diagram in the DOT file output. Default is "TB" for top-to-bottom.
Other choices are "LR" for left-to-right plus "BT" (bottom-top) and "RL" (right-left).

--libpath=relative-path-to-library

The directory containing the readgedcom library, relative to the drawing program. Default is ".", the same location as this program file.


## Examples ##

For a standard bowtie chart the descendents are from the middle person
```
draw-bowtie-plus.py --from=0 --descendents=100  family.ged  middlepersonxref >chart.dot 2>chart.err
```

For a list of only ancestors
```
draw-bowtie-plus.py --descendents=0  family.ged  middlepersonxref >chart.dot 2>chart.err
```

For a list of only descendents
```
draw-bowtie-plus.py --from=0 --ancestors=0 --descendents=100  family.ged  middlepersonxref >chart.dot 2>chart.err
```

For all ancestors and cousins (including aunts and uncles)
```
draw-bowtie-plus.py --from=2 --descendents=2  family.ged  middlepersonxref >chart.dot 2>chart.err
```

For middleperson's parents and siblings
```
draw-bowtie-plus.py --from=1 --ancestors=1 --descendents=1  family.ged  middlepersonxref >chart.dot 2>chart.err
```

To use the REFN tag to identify the middle person
```
draw-bowtie-plus.py --iditem=refn  family.ged  personrefn >chart.dot 2>chart.err
```

## Test Results ##

Look in the test-output directory for working examples with results.

For example, using the Skywalker family display Leia's cousins with these options (test no.5)
```
--anc=2 --from=2 --desc=2
```

Except that she has no cousins, but it does show her brother and aunt:
![Test no.5](test-output/5.png)

## Bugs ##

Families not attached to the middle person might appear if its a second marriage of an ancestor.

## Bug reports ##

This code is provided with neither support nor warranty.

## Future Enhancements ##

- number of descendendents of middle person should be separated from generation count from ancestors 
- other output formats (gedcom, graphml )
- skip adoption relations
