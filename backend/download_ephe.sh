#!/bin/bash

# Create ephe directory
mkdir -p backend/astrology/ephe

# Download Swiss Ephemeris files
cd backend/astrology/ephe

# Download the files from astro.com
curl -L https://www.astro.com/swisseph/swephfiles/sepl_18.se1 -o sepl_18.se1
curl -L https://www.astro.com/swisseph/swephfiles/semo_18.se1 -o semo_18.se1
curl -L https://www.astro.com/swisseph/swephfiles/seas_18.se1 -o seas_18.se1

# Verify files were downloaded
ls -l *.se1 