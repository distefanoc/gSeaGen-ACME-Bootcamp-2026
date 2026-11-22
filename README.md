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

## Hands-on exercises

Instructions, simulation scripts and analysis examples will be provided in this repository.

- [Atmospheric neutrinos: REAL vs WEIGHTED generation](exercises/atmospheric-neutrinos.md)
- [Exercise 3: Atmospheric and astrophysical neutrino flux reweighting](exercises/Exercise3.md)

## Useful links

- [gSeaGen source code (GitLab)](https://git.km3net.de/opensource/gseagen)
- [GENIE Neutrino Monte Carlo Generator](https://genie-mc.org/)
- [Apptainer](https://apptainer.org/)
- [ROOT](https://root.cern/)
