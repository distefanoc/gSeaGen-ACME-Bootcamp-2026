# Exercise 3 — Atmospheric and astrophysical neutrino flux reweighting

## Learning objectives

Use a single Monte Carlo sample generated with gSeaGen to calculate event rates corresponding to different neutrino flux models.

We will compare an atmospheric neutrino flux based on the Wang–Yasuda parametrization with a simple astrophysical power-law spectrum.

The aim is to understand how the same simulated events can be reused for different physical flux hypotheses by changing their weights.

## Scripts used in this exercise

Open these scripts during the exercise to explore the simulation configuration, the atmospheric neutrino flux model, and the event reweighting procedure.

**Simulation script:**

- [`run_gseagen_diffuse.sh`](../scripts/run_gseagen_diffuse.sh) — Generate a diffuse sample of muon neutrinos and antineutrinos (PDG 14 and -14) with an $E^{-2}$ spectrum.

**Analysis scripts:**

- [`atmospheric_flux.py`](../scripts/atmospheric_flux.py) — Calculate the atmospheric neutrino flux using the Wang–Yasuda parametrization.
- [`plot_atmo_cosmic_reweight.py`](../scripts/plot_atmo_cosmic_reweight.py) — Reweight the generated events using different flux models and compare the resulting energy distributions and event rates.

## 1. Generate a diffuse neutrino sample

From the top-level directory of the repository, run:

```bash
bash scripts/run_gseagen_diffuse.sh
```

The script generates muon neutrinos and antineutrinos (PDG 14 and -14) with energies between 100 GeV and 1 PeV, using the flux

\[
\Phi(E)=10^{-5}E^{-2}
\]

where energy is in GeV and the flux is in GeV⁻¹ m⁻² s⁻¹ sr⁻¹, separately for each neutrino species.

The generated ROOT file is:

`files/atmo_cosmic_reweight.1.et.root`

## 2. Reweight the events

The gSeaGen output contains the information needed to calculate event rates for different flux hypotheses.

For the original flux, the event rate is obtained using

\[
w_{\mathrm{original}}=\frac{\mathrm{EvtWeight}}{N_{\mathrm{tot}}}.
\]

For a different flux model,

\[
w_{\mathrm{target}}=
\frac{\mathrm{GenWeight}}{N_{\mathrm{tot}}}
\Phi_{\mathrm{target}}(E,\theta,\mathrm{PDG}).
\]

We will use the Wang–Yasuda parametrization to calculate atmospheric neutrino weights.

## 3. Compare the two flux hypotheses

From the top-level directory of the repository, run:

```bash
python3 scripts/plot_atmo_cosmic_reweight.py
```

The script reads the same Monte Carlo sample and calculates event rates for the original power-law flux and the atmospheric flux.

The resulting plot is saved as:

`plots/atmo_cosmic_reweight.png`

The plot shows the total contribution and the separate contributions from muon neutrinos and antineutrinos.

## 4. Questions

1. Why can the same Monte Carlo sample be used for different neutrino flux hypotheses?
2. What is the difference between `GenWeight` and `EvtWeight`?
3. Why are the neutrino and antineutrino event rates different?
4. How does changing the flux model affect the energy distribution of the expected events?

## Note

The flux models used here are intended to illustrate the event reweighting procedure. A realistic physics analysis would require more accurate flux models.
