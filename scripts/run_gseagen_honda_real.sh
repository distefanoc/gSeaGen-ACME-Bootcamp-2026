#!/bin/bash

source setup.sh

mkdir -p files

OPTIONS=(
    -n -1
    -e 100,10000
    -t -1.,1.
    -f "HONDA:/builds/opensource/gseagen/dat/grn-ally-20-12-solmin.d[14,-14]"
    -c CAN:0.00,1027.00,888.40
    -d 3500
    -r 1
    -o files/honda_real
    --coord SITE:ARCA
    --time "1609459200,1609545600"
    --tune GHE19_00b_00_000
    --event-generator-list CCHEDIS
    --wgt 0
)

/usr/bin/time -p apptainer exec "$CONTAINER" gSeaNuEvGen "${OPTIONS[@]}"
