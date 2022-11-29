# draw-bowtie-plus
Genealogical bowtie chart with more options for descendents.

## Installation ##

- Requires python 3.6+
- Copy draw-bowtie-plus.py
- also requires gedcom library [readgedcom.py](https://github.com/johnandrea/readgedcom)

## Usage ##

Run the program with:
```
diff.py  family.ged  personxref >chart.dot 2>chart.err
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

--reverse

Reverse the order of the arrows between parents and children.

--libpath=relative-path-to-library

The directory containing the readgedcom library, relative to the . Default is ".", the same location as this program file.


## Examples ##

For a standard bowtie chart the descendents are from the middle person
```
draw-bowtie-plus.py --from=0 --descendents=100  family.ged  middlepersonxref
```

For a list of only ancestors
```
draw-bowtie-plus.py --descendents=0  family.ged  middlepersonxref
```

For a list of only descendents
```
draw-bowtie-plus.py --from=0 --ancestors=0 --descendents=100  family.ged  middlepersonxref
```

For all ancestors and cousins (including aunts and uncles)
```
draw-bowtie-plus.py --from=2 --descendents=2  family.ged  middlepersonxref
```

For parents and siblings
```
draw-bowtie-plus.py --from=1 --ancestors=1 --descendents=1  family.ged  middlepersonxref
```
