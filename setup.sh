#!/bin/bash

# gSeaGen release configuration
export GSEAGEN_VERSION="v7.7.1"
export ZENODO_RECORD="24232207"

# Container information
export CONTAINER="gseagen_open_${GSEAGEN_VERSION}.sif"
export CONTAINER_MD5="78a42495dbc5b42eb1aa83cb04bc7a84"

# Download URLs
export ZENODO_URL="https://zenodo.org/records/${ZENODO_RECORD}"
export CONTAINER_URL="${ZENODO_URL}/files/${CONTAINER}?download=1"
