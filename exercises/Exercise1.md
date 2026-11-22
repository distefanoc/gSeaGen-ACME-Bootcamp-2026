# Exercise 1 – Simulation of a diffuse neutrino flux

In this exercise, we will simulate charged-current interactions of muon neutrinos from an isotropic flux with an $E^{-2}$ energy spectrum, using a detector geometry inspired by KM3NeT/ARCA.

## 1.1 Run the simulation with one energy bin

From your working directory, load the configuration:

```bash
source setup.sh
```

Start the simulation:

```bash
time bash scripts/run_gseagen_numuCC_1bin.sh
```

### While the simulation is running...

Open a second terminal in the working directory and examine [run_gseagen_numuCC_1bin.sh](../scripts/run_gseagen_numuCC_1bin.sh).

Try to identify:

- The neutrino energy range and the number of neutrinos to generate.
- The neutrino flavour and the energy dependence of the flux.
- The detector geometry and the angular range.
- The interaction processes and the number of energy bins.
- The meaning of weighted event generation.

When the simulation finishes, check the output files:

```bash
ls -lh files/numuCC_1bin*
```

Inspect the generation statistics:

```bash
cat files/numuCC_1bin.1.binstat
```

**Questions:**

- What is the energy range of the simulation?
- What is the mean number of neutrinos to simulate?
- How many neutrinos were actually simulated?
- How many events were saved?
- How long did the simulation take (real elapsed time)?

## 1.2 Run the simulation with five energy bins

Now repeat the generation using five energy bins:

```bash
time bash scripts/run_gseagen_numuCC_5bin.sh
```

### While the simulation is running...

Open the Python analysis script [plot_neutrino.py](../scripts/plot_neutrino.py) and examine its structure.

Try to identify:

- How the generation parameters and simulated events are read from the ROOT file.
- Which quantities are plotted in the four histograms.
- The difference between weighted and unweighted distributions.
- How the total event rate and the expected number of events per year are calculated.

In the second terminal, from the working directory, load the configuration and run the analysis on the **one-bin** simulation output while the five-bin simulation is still running:

```bash
source setup.sh
apptainer exec "$CONTAINER" python3 -i scripts/plot_neutrino.py files/numuCC_1bin.1.et.root
```

Inspect the energy and zenith-angle distributions, both weighted and unweighted, and the event rates printed by the script. Exit Python with `exit()` when you are finished.

When the five-bin simulation finishes, check its output files and generation statistics:

```bash
ls -lh files/numuCC_5bin*
cat files/numuCC_5bin.1.binstat
```

**Questions:**

- How many events were saved with five energy bins?
- How do the generation statistics compare with the one-bin simulation?
- How does the elapsed generation time compare with the one-bin simulation, and how does the number of saved events change?

## 1.3 Analyse and compare the results

You have already analysed the one-bin sample. Now run the same script on the five-bin output:

```bash
apptainer exec "$CONTAINER" python3 -i scripts/plot_neutrino.py files/numuCC_5bin.1.et.root
```

Compare the unweighted and weighted neutrino energy and zenith-angle distributions, as well as the total event rates.

**Questions:**

- How do the weighted and unweighted distributions differ?
- What changes when using five energy bins instead of one?
- Are the estimated event rates compatible, taking statistical fluctuations into account?

### Compare the weighted distributions directly

Run [compare_neutrino.py](../scripts/compare_neutrino.py) to overlay the weighted energy and zenith-angle distributions from the one-bin and five-bin simulations:

```bash
apptainer exec "$CONTAINER" python3 -i scripts/compare_neutrino.py files/numuCC_1bin.1.et.root files/numuCC_5bin.1.et.root
```

Inspect the two panels in `plots/compare_neutrino.png`. The blue points correspond to one energy bin and the red points to five energy bins; the error bars show statistical uncertainties. The terminal also prints the saved event counts, the estimated event rates and their ratio (5 bins / 1 bin).

**Questions:**

- Are the two weighted distributions consistent within statistical fluctuations?
- What is the ratio of the estimated event rates?
- Why does the five-bin simulation produce more saved events while giving a consistent physical event rate?
