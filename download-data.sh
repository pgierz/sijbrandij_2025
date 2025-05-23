#!/bin/bash -e
###############################################################################
#
# Downloads the accompanying data from Zenodo
# 10.5281/zenodo.15497082
#
# Dr. Paul Gierz
# AWI Bremerhaven
###############################################################################

wget -O data.zip https://zenodo.org/api/records/15497082/files-archive
