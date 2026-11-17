# Exercise 1 – Simulation of a diffuse neutrino flux

In this exercise, we will simulate charged-current interactions of muon neutrinos from an isotropic flux with an $E^{-2}$ energy spectrum, using a detector geometry inspired by KM3NeT/ARCA.

## 1.1 Run the simulation

From your working directory, load the configuration:

```bash
source setup.sh
```

Open the simulation script [run_gseagen_numuCC_1bin.sh](../scripts/run_gseagen_numuCC_1bin.sh) and inspect the generation parameters.

Run the simulation:

```bash
bash scripts/run_gseagen_numuCC_1bin.sh
```

Check the output files:

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
