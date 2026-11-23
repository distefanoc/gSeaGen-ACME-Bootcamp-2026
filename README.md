# gSeaGen – ACME Neutrino Astronomy School 2026

Hands-on sessions on neutrino event simulation with gSeaGen.

**ACME Neutrino Astronomy School**  
Aussois, France – November 29–December 4, 2026

## Overview

The aim of these hands-on sessions is to introduce students to Monte Carlo simulations of neutrino interactions using gSeaGen, a neutrino event generator based on GENIE.

Students will learn how to generate neutrino events and analyse the simulation output using ROOT and Python.

## Software setup

We will use gSeaGen distributed as an Apptainer container that includes all the required software and dependencies.

The gSeaGen version used during the hands-on sessions is specified in the [setup.sh](setup.sh) configuration file.

Please complete the software setup **before the school** by following the instructions for your operating system:

- [Linux](setup/Linux.md)
- [macOS](setup/macOS.md)
- [Windows](setup/Windows.md)

Once Apptainer has been successfully installed, follow these instructions:

- [Downloading and testing gSeaGen](setup/gSeaGen.md)

### PowerPoint summary (optional)

To create a PowerPoint presentation collecting the plots produced during the hands-on exercises, install `python-pptx` on your Linux system or virtual machine (**outside the Apptainer container**). On Ubuntu, run:

```bash
sudo apt update
sudo apt install python3-pip
python3 -m pip install python-pptx
```

Then, from the main directory of this repository, run:

```bash
python3 scripts/create_summary_pptx.py
```

This creates `gseagen_hands_on_results.pptx` in the main directory. Only plots already available in `plots/` are included, so you can run the script before completing all the exercises and rerun it later to update the presentation. The generated PowerPoint is not tracked by Git.

## Hands-on exercises

Instructions, simulation scripts and analysis examples will be provided in this repository.

- [Exercise 1: Simulation of a diffuse neutrino flux](exercises/Exercise1.md)
- [Exercise 2: Simulation of an astrophysical neutrino source](exercises/Exercise2.md)
- [Exercise 3: Atmospheric neutrinos: REAL vs WEIGHTED generation](exercises/Exercise3.md)
- [Exercise 4: Atmospheric and astrophysical neutrino flux reweighting](exercises/Exercise4.md)
- [Exercise 5: Neutrino transmission through the Earth](exercises/Exercise5.md)

## Useful links

- [gSeaGen source code (GitLab)](https://git.km3net.de/opensource/gseagen)
- [GENIE Neutrino Monte Carlo Generator](https://genie-mc.org/)
- [Apptainer](https://apptainer.org/)
- [ROOT](https://root.cern/)
