#!/bin/bash

source setup.sh

mkdir -p files

OPTIONS=(
    -n 100000
    -e 100,10000
    -t -1.,1.
    -b 5
    -a 1.4
    -f "HONDA:/builds/opensource/gseagen/dat/grn-ally-20-12-solmin.d[14,-14]"
    -c CAN:0.00,1027.00,888.40
    -d 3500
    -r 1
    -o files/honda_weighted
    --coord SITE:ARCA
    --time "1609459200,1609545600"
    --event-generator-list CCHEDIS
    --tune GHE19_00b_00_000
    --wgt 2
)

/usr/bin/time -p apptainer exec "$CONTAINER" gSeaNuEvGen "${OPTIONS[@]}"
