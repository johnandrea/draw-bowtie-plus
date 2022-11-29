# draw-bowtie-plus
Genealogical bowtie chart with more options for descendents.

## Installation ##

- Requires python 3.6+
- Copy draw-bowtie-plus.py
- also requires gedcom library [readgedcom.py](https://github.com/johnandrea/readgedcom)
- Output makes use of Graphviz DOT format: [Graphviz](https://graphviz.org)

## Usage ##

Run the program with:
```
diff.py  family.ged  personxref >chart.dot 2>chart.err
graphviz -Tpng chart.dot -o chart.png
graphviz -Tsvg chart.dot -o chart.svg
```

where personxref is the gedcom id of the person in the middle of the bowtie.

## Options ##

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

## Bug reports ##

This code is provided with neither support nor warranty.

## Future Enhancements ##

- other output formats (gedcom, graphml )
- skip adoption relations
