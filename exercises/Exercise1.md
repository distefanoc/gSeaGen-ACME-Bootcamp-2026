# Exercise 1 – Simulation of a diffuse neutrino flux

In this exercise, we will simulate charged-current interactions of muon neutrinos from an isotropic flux with an $E^{-2}$ energy spectrum, using a detector geometry inspired by KM3NeT/ARCA.

## 1.1 Run the simulation with one energy bin

From your working directory, load the configuration:

```bash
source setup.sh
```

Start the simulation:

```bash
bash scripts/run_gseagen_numuCC_1bin.sh
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

## 1.2 Run the simulation with five energy bins

Now repeat the generation using five energy bins:

```bash
bash scripts/run_gseagen_numuCC_5bin.sh
```

### While the simulation is running...

Open the Python analysis script [plot_neutrino.py](../scripts/plot_neutrino.py) and examine its structure.

Try to identify:

- How the generation parameters and simulated events are read from the ROOT file.
- Which quantities are plotted in the four histograms.
- The difference between weighted and unweighted distributions.
- How the total event rate and the expected number of events per year are calculated.

We will use this script to analyse the simulation results.

When the simulation finishes, check the output files and generation statistics:

```bash
ls -lh files/numuCC_5bin*
cat files/numuCC_5bin.1.binstat
```

**Questions:**

- How many events were saved with five energy bins?
- How do the generation statistics compare with the one-bin simulation?

## 1.3 Analyse and compare the results

Run the analysis script on each simulation output:

```bash
apptainer exec "$CONTAINER" python3 -i scripts/plot_neutrino.py files/numuCC_1bin.1.et.root
```

After inspecting the plots and printed results, exit Python with `exit()`, then analyse the five-bin sample:

```bash
apptainer exec "$CONTAINER" python3 -i scripts/plot_neutrino.py files/numuCC_5bin.1.et.root
```

Compare the unweighted and weighted neutrino energy and zenith-angle distributions, as well as the total event rates.

**Questions:**

- How do the weighted and unweighted distributions differ?
- What changes when using five energy bins instead of one?
- Are the estimated event rates compatible, taking statistical fluctuations into account?
