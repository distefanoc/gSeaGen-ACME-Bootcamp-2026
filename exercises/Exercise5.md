# Exercise 5 — Neutrino transmission through the Earth

## Learning objectives

Explore how the Earth becomes less transparent to neutrinos as their energy increases, and how the transmission probability depends on the arrival direction.

In this exercise, we will use two applications provided by gSeaGen, `gCalcPEarth` and `gPlotPEarth`, to calculate and plot the neutrino transmission probability through the Earth, without generating Monte Carlo events.

By the end of this exercise, you will be able to:

- Use gSeaGen applications to study neutrino transmission through the Earth.
- Calculate the Earth transmission probability with `gCalcPEarth`.
- Visualize its dependence on neutrino energy and direction using `gPlotPEarth`.
- Interpret the differences between neutrinos and antineutrinos.

## Applications used in this exercise

- `gCalcPEarth` — Calculate the probability for neutrinos to cross the Earth without undergoing the interactions included in the calculation.
- `gPlotPEarth` — Visualize the resulting transmission probabilities.

## 5.1 Calculate the Earth transmission probability

From the top-level directory of the repository, load the configuration (if you have not already done so):

```bash
source setup.sh
```

This defines `$CONTAINER` and creates the `files/` and `plots/` directories. The gSeaGen applications run inside the Apptainer container using `apptainer exec`.

Run:

```bash
apptainer exec "$CONTAINER" gCalcPEarth -o files/pearth.root
```

The default configuration uses the GENIE tune `GHE19_00b_00_000`, a detector depth of 3500 m and a cross-section scaling factor of `k = 1`. The calculation covers all neutrino and antineutrino flavours.

The output is saved in `files/pearth.root`.

## 5.2 Plot and interpret the results

Use `gPlotPEarth` to produce three complementary views of the same calculation. The `png` output format is supported by the version used in this exercise, even though it is not listed in the help message.

Run these commands from the repository's top-level directory:

```bash
apptainer exec "$CONTAINER" gPlotPEarth -i files/pearth.root -p 1 -f png
mv pearth.png plots/pearth_2d.png

apptainer exec "$CONTAINER" gPlotPEarth -i files/pearth.root -p 2 -f png
mv pearth.png plots/pearth_vs_energy.png

apptainer exec "$CONTAINER" gPlotPEarth -i files/pearth.root -p 3 -f png
mv pearth.png plots/pearth_vs_costheta.png
```

The three figures show:

- **`plots/pearth_2d.png`** — Two-dimensional maps of the transmission probability versus neutrino energy and zenith-angle cosine.
- **`plots/pearth_vs_energy.png`** — Transmission probability versus energy for different directions.
- **`plots/pearth_vs_costheta.png`** — Transmission probability versus zenith-angle cosine for different energies.

**Questions:**

- How does the transmission probability change as the neutrino energy increases?
- What is the difference between neutrinos arriving from above and neutrinos crossing the Earth?
- Why does the transmission probability depend on the zenith angle?
- How do neutrino and antineutrino probabilities compare?
- Can you identify the feature associated with the Glashow resonance in the electron antineutrino results?

**Note:** This calculation does not describe full neutrino transport with regeneration. In particular, it does not include tau-neutrino regeneration through charged-current interactions followed by tau decay.

## Further exploration

Explore the `gCalcCross` application provided by gSeaGen to investigate how neutrino interaction cross sections depend on energy and interaction type.

---

[Back to the main page](https://github.com/distefanoc/gSeaGen-ACME-Bootcamp-2026/blob/main/README.md#hands-on-exercises)
