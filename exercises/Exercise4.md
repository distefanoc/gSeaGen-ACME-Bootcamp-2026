# Exercise 4 — Atmospheric and astrophysical neutrino flux reweighting

## Learning objectives

Use a single Monte Carlo sample generated with gSeaGen to calculate event rates corresponding to different neutrino flux models.

We will compare an atmospheric neutrino flux based on the Wang–Yasuda parametrization with a simple astrophysical power-law spectrum.

The aim is to understand how the same simulated events can be reused for different physical flux hypotheses by changing their weights.

## Scripts used in this exercise

Open these scripts during the exercise to explore the simulation configuration, the atmospheric neutrino flux model, and the event reweighting procedure.

**Simulation script:**

- [`run_gseagen_diffuse.sh`](../scripts/run_gseagen_diffuse.sh) — Generate a diffuse sample of muon neutrinos and antineutrinos (PDG 14 and -14) with an $E^{-2}$ spectrum.

**Analysis scripts:**

- [`plot_honda_wang_yasuda.py`](../scripts/plot_honda_wang_yasuda.py) — Compare the Honda and Wang–Yasuda atmospheric flux models over their common energy range.
- [`atmospheric_flux.py`](../scripts/atmospheric_flux.py) — Calculate the atmospheric neutrino flux using the Wang–Yasuda parametrization.
- [`plot_atmo_cosmic_reweight.py`](../scripts/plot_atmo_cosmic_reweight.py) — Reweight the generated events using different flux models and compare the resulting energy distributions and event rates.

## 4.1 Generate a diffuse neutrino sample

From the top-level directory of the repository, run:

```bash
bash scripts/run_gseagen_diffuse.sh
```

The script generates muon neutrinos and antineutrinos (PDG 14 and -14) with energies between 100 GeV and 1 PeV, using the flux

$$
\Phi(E)=10^{-5}E^{-2}
$$

where energy is in GeV and the flux is in GeV⁻¹ m⁻² s⁻¹ sr⁻¹. The same flux is used for both muon neutrinos and antineutrinos.

The generated ROOT file is:

`files/atmo_cosmic_reweight.1.et.root`

## 4.2 Compare Honda and Wang–Yasuda

The Honda atmospheric neutrino flux tables used in Exercise 3 extend up to 10 TeV, whereas the diffuse sample generated here covers energies up to 1 PeV. Before reweighting the sample over the full energy range, compare the Honda flux with the analytical Wang–Yasuda parametrization in their common energy interval, 100 GeV–10 TeV.

**Note:** This script uses the Honda WEIGHTED sample from Exercise 3. Make sure you have either copied the pre-generated ROOT file from `samples/` to `files/` or generated it yourself using the script provided in Exercise 3.

From the top-level directory of the repository, run:

```bash
python3 scripts/plot_honda_wang_yasuda.py
```

The script compares the expected event rates for the total sample and separately for muon neutrinos and antineutrinos. It also shows the Wang–Yasuda/Honda ratio.

The resulting plot is saved as:

`plots/honda_wang_yasuda.png`

This comparison motivates the use of Wang–Yasuda for the following reweighting exercise, while keeping in mind the limitations of the parametrization at high energies.

## 4.3 Reweight the events

The gSeaGen output contains the information needed to calculate event rates for different flux hypotheses.

For the original flux, the event rate is obtained using

$$
w_{\mathrm{original}}=\frac{\mathrm{EvtWeight}}{N_{\mathrm{tot}}}.
$$

For a different flux model,

$$
w_{\mathrm{target}}=
\frac{\mathrm{GenWeight}}{N_{\mathrm{tot}}}
\Phi_{\mathrm{target}}(E,\theta,\mathrm{PDG}).
$$

We will use the Wang–Yasuda parametrization of the conventional atmospheric muon neutrino flux, which includes contributions from pion and kaon decays.

gSeaGen supports the use of atmospheric neutrino flux tables, such as Honda, and examples are available in the gSeaGen documentation. However, the Honda tables used here extend only up to 10 TeV, while our simulated energy range reaches 1 PeV. For this exercise, we therefore use the analytical Wang–Yasuda parametrization to calculate the atmospheric flux over the full energy range, keeping in mind its limitations at high energies.

The atmospheric flux is calculated by the function `atmospheric_numu_flux()` implemented in [`atmospheric_flux.py`](../scripts/atmospheric_flux.py). This function is called by `plot_atmo_cosmic_reweight.py` to calculate the new event weights.

The parametrization describes the atmospheric flux at the Earth's surface and does not include neutrino absorption in the Earth, oscillations, or the prompt component.

**Reference:** Y. Wang and O. Yasuda, *Search for sterile neutrinos by shower events at a future neutrino telescope*, Progress of Theoretical and Experimental Physics **2022**, 023B04 (2022), Section 4.1.1, Eq. (54). [DOI: 10.1093/ptep/ptac010](https://doi.org/10.1093/ptep/ptac010).

## 4.4 Compare the two flux hypotheses

From the top-level directory of the repository, run:

```bash
python3 scripts/plot_atmo_cosmic_reweight.py
```

The script reads the same Monte Carlo sample and calculates event rates for the original power-law flux and the atmospheric flux.

The resulting plot is saved as:

`plots/atmo_cosmic_reweight.png`

The plot shows the total contribution and the separate contributions from muon neutrinos and antineutrinos.

## 4.5 Questions

1. Why can the same Monte Carlo sample be used for different neutrino flux hypotheses?
2. What is the difference between `GenWeight` and `EvtWeight`?
3. Why are the neutrino and antineutrino event rates different?
4. How does changing the flux model affect the energy distribution of the expected events?

## Note

The Wang–Yasuda parametrization is an approximation and is not intended for precision predictions, particularly at high energies.

**Further exercise:** Try replacing the Wang–Yasuda parametrization with a more realistic atmospheric neutrino flux, for example using Daemonflux, a data-driven model calibrated with atmospheric muon measurements. Compare the resulting energy distributions and event rates.

**Alternative approach:** gSeaGen can also read user-defined neutrino fluxes provided as ROOT `TGraph` objects and calculate the corresponding event weights directly during generation. This allows more realistic flux models to be used without implementing the flux calculation in the analysis script.

---

[Back to the main page](https://github.com/distefanoc/gSeaGen-ACME-Bootcamp-2026/blob/main/README.md#hands-on-exercises)
