# Exercise 2 – Simulation of an astrophysical neutrino source

## Learning objectives

In this exercise, we will simulate muon neutrinos from RX J1713.7−3946, first as a point-like source and then as an extended source with an angular radius of 0.6°. We will use the same detector geometry in both simulations and explore the reconstructed directions of the *generated* neutrinos in equatorial coordinates.

By the end of this exercise, you will be able to:

- Configure a point-like or extended astrophysical neutrino source in gSeaGen.
- Identify the source position, angular extension, and generation time interval in the simulation inputs.
- Convert neutrino propagation directions into equatorial coordinates (right ascension and declination).
- Compare the angular distributions produced by point-like and extended source models.

**Note:** The simulation scripts currently use a simple test flux proportional to $E^{-2}$, not a physical spectrum fitted to RX J1713.7−3946. This exercise focuses on the *spatial* distribution; we will not calculate an astrophysical event rate here.

## Scripts and configuration files used in this exercise

Open these files during the exercise to explore the source configuration, simulation parameters, and analysis steps.

**Source configuration files:**

- [`rxj1713_point.xml`](../data/rxj1713_point.xml) — Define the point-like source.
- [`rxj1713_extended.xml`](../data/rxj1713_extended.xml) — Define the extended source with an angular radius of 0.6°.

**Simulation scripts:**

- [`run_gseagen_rxj1713_point.sh`](../scripts/run_gseagen_rxj1713_point.sh) — Generate neutrino interactions from the point-like source.
- [`run_gseagen_rxj1713_extended.sh`](../scripts/run_gseagen_rxj1713_extended.sh) — Generate neutrino interactions from the extended source.

**Analysis script:**

- [`plot_astro_source.py`](../scripts/plot_astro_source.py) — Plot the neutrino arrival directions in J2000 equatorial coordinates for either source configuration.

## 2.1 Simulate a point-like source

From the repository's working directory, load the configuration:

```bash
source setup.sh
```

Examine the source definition in [rxj1713_point.xml](../data/rxj1713_point.xml) and the generation script [run_gseagen_rxj1713_point.sh](../scripts/run_gseagen_rxj1713_point.sh).

Try to identify:

- The source coordinates (right ascension and declination), their reference epoch, and the angular radius.
- The neutrino energy range, flux function, and neutrino flavour.
- The generation time interval and detector location.
- The number of energy bins and the interaction model.

Start the simulation:

```bash
time bash scripts/run_gseagen_rxj1713_point.sh
```

When it finishes, check the output:

```bash
ls -lh files/rxj1713_point*
cat files/rxj1713_point.1.binstat
```

**Questions:**

- What makes this source point-like in the input file?
- What period of observation is simulated?
- How many events were saved?

## 2.2 Plot the neutrino directions

Examine [plot_astro_source.py](../scripts/plot_astro_source.py). The script reads the source coordinates and detector location from the ROOT header and converts the neutrino propagation directions into equatorial coordinates using gSeaGen's astronomical utilities. It then expresses the directions in the J2000 reference frame.

During event generation, gSeaGen accounts for precession and nutation. The plotting script includes two functions, `inverse_nutation()` and `inverse_precession()`, to reverse these corrections using the time of each event, since the corresponding inverse transformations are not yet implemented in gSeaGen.

Run the analysis:

```bash
apptainer exec "$CONTAINER" python3 scripts/plot_astro_source.py files/rxj1713_point.1.et.root
```

The script saves the figure in `plots/rxj1713_point.1.png`. Press Enter in the terminal when you are ready to close the plot.

The plot shows the neutrino arrival directions as black points and the J2000 source position as a red open circle.

**Questions:**

- Why must the neutrino propagation direction be reversed to point towards the source?
- How do the reconstructed neutrino directions compare with the J2000 source position?

## 2.3 Simulate and compare an extended source

Now examine [rxj1713_extended.xml](../data/rxj1713_extended.xml) and [run_gseagen_rxj1713_extended.sh](../scripts/run_gseagen_rxj1713_extended.sh).

Compare these files with the point-source configuration. The source coordinates remain the same, but its angular radius is now **0.6°**.

Run the extended-source simulation:

```bash
time bash scripts/run_gseagen_rxj1713_extended.sh
```

Check the output:

```bash
ls -lh files/rxj1713_extended*
cat files/rxj1713_extended.1.binstat
```

Plot the directions using the **same** analysis script:

```bash
apptainer exec "$CONTAINER" python3 scripts/plot_astro_source.py files/rxj1713_extended.1.et.root
```

The figure is saved as `plots/rxj1713_extended.1.png`. Compare it with `plots/rxj1713_point.1.png`.

**Questions:**

- How does the angular distribution change when the source radius increases from 0° to 0.6°?
- Does the source's reference position change?
- What information does the plotting script obtain automatically from the ROOT header?
- Why is it useful to display both simulations with a common angular scale?

The plotting script displays a field of at least ±1° around the J2000 source position, allowing a consistent visual comparison of these two configurations.
