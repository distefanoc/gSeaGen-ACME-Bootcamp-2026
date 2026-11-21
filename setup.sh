#!/bin/bash

# gSeaGen release configuration
export GSEAGEN_VERSION="v7.7.2"
export ZENODO_RECORD="24429854"

# Container information
export CONTAINER="gseagen_open_${GSEAGEN_VERSION}.sif"
export CONTAINER_MD5="f2b28339cf07883c9feeba594640b81b"

# Download URLs
export ZENODO_URL="https://zenodo.org/records/${ZENODO_RECORD}"
export CONTAINER_URL="${ZENODO_URL}/files/${CONTAINER}?download=1"

# Create output directories in the working directory
mkdir -p files plots
