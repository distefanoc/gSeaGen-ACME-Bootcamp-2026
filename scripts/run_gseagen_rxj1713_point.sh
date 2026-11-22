#!/bin/bash

source setup.sh

OPTIONS=(
    -n 5E4                           # Number of neutrinos to generate
    -e 1E2,1E6                       # Neutrino energy range (GeV)
    -f "FUNC1:1E-5*pow(x,-2)[14]"    # TEMPORARY test flux; replace with RX J1713 physical spectrum
    -c "CAN:0.00,1027.00,888.40"     # Can geometry: Zmin,Zmax,Radius (m)
    -r 1                             # Run number
    -b 5                             # Number of energy bins
    -o "files/rxj1713_point"         # Output file name prefix
    --event-generator-list CCHEDIS   # Interaction processes
    --tune GHE19_00b_00_000          # GENIE physics tune
    -d 3500.                         # Sea depth (m)
    --coord "RAD:0.632973,0.280998"  # Detector latitude and longitude (rad)
    --rt "proj"                      # Projected generation area
    --wgt 2                          # Weighted event generation
    --time "1609459200,1640991599"   # Generation period: year 2021 (Unix timestamps)
    --point "FILE:data/rxj1713_point.xml"  # Astrophysical point source
)

apptainer exec "$CONTAINER" gSeaNuEvGen "${OPTIONS[@]}"
