# gSeaGen – ACME Neutrino Astronomy Bootcamp 2026

Hands-on sessions on neutrino event simulation with gSeaGen.

**ACME Neutrino Astronomy Bootcamp**  
Aussois, France – November 29–December 4, 2026

## Overview

The aim of these hands-on sessions is to introduce students to Monte Carlo simulations of neutrino interactions using gSeaGen, a neutrino event generator based on GENIE.

Students will learn how to generate neutrino events and analyse the simulation output using ROOT and Python.

## Software setup

We will use gSeaGen distributed as an Apptainer container that includes all the required software and dependencies.

The gSeaGen version used during the hands-on sessions is specified in the [setup.sh](setup.sh) configuration file.

Please complete the software setup **before the bootcamp** by following the instructions for your operating system:

- [Linux](setup/Linux.md)
- [macOS](setup/macOS.md)
- [Windows](setup/Windows.md)

Once Apptainer has been successfully installed, follow these instructions:

- [Downloading and testing gSeaGen](setup/gSeaGen.md)

To prepare the optional PowerPoint summary, follow these installation instructions:

- [Installing python-pptx](setup/PowerPoint.md)

## Hands-on exercises

Instructions, simulation scripts and analysis examples will be provided in this repository.

- [Exercise 1: Simulation of a diffuse neutrino flux](exercises/Exercise1.md)
- [Exercise 2: Simulation of an astrophysical neutrino source](exercises/Exercise2.md)
- [Exercise 3: Atmospheric neutrinos: REAL vs WEIGHTED generation](exercises/Exercise3.md)
- [Exercise 4: Atmospheric and astrophysical neutrino flux reweighting](exercises/Exercise4.md)
- [Exercise 5: Neutrino transmission through the Earth](exercises/Exercise5.md)

You can also generate a PowerPoint presentation summarizing your results:

- [Generating a PowerPoint summary](exercises/PowerPoint.md)

## Useful links

- [gSeaGen source code (GitLab)](https://git.km3net.de/opensource/gseagen)
- [GENIE Neutrino Monte Carlo Generator](https://genie-mc.org/)
- [Apptainer](https://apptainer.org/)
- [ROOT](https://root.cern/)
