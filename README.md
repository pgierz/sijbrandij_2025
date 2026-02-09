# Proglacial Lakes Substantially Modulate the Surface Mass Balance of Retreating Ice Sheets

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pgierz/sijbrandij_2025/HEAD?urlpath=lab/tree/README.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15497082.svg)](https://doi.org/10.5281/zenodo.15497082)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Authors:** Lianne Sijbrandij, Paul Gierz, Uta Krebs-Kanzow

This repository contains scripts and analysis code to reproduce all figures and tables from Sijbrandij et al. (2025).

## Quick Start

Reproduce all figures directly in your browser via Binder -- no local installation required.

## Repository Structure

```
.
├── scripts/          # Figure generation scripts (Jupyter notebooks, Python, MATLAB)
├── figures/          # Generated figure outputs
├── environment.yml   # Conda environment specification
└── download-data.sh  # Script to fetch data from Zenodo
```

## Experiment Name Mapping

The scripts use internal experiment identifiers that differ from the manuscript:

| Manuscript ID | Internal Name   |
|---------------|-----------------|
| `alakeGLAC`   | `REF13ka`       |
| `alake13ka`   | `PL13ka_{warm}` |
| `plake`       | `PL13ka`        |

## Data

Model output data is archived on Zenodo. Download with:

```bash
./download-data.sh
```

## Local Installation

### Requirements

- Python 3.x with: matplotlib, numpy, netCDF4, cartopy, xarray, scipy, cmocean
- CDO (Climate Data Operators)
- MATLAB (for `Fig3_and_Tabs.m`, `FigS7.m`, and supplementary figures)

### Setup

```bash
conda env create -f environment.yml
conda activate sijbrandij_2025
```

## Scripts Overview

| Script | Output |
|--------|--------|
| `Fig1_echam_T2m.ipynb` | Figure 1 (temperature) |
| `Fig1_echam_precip.ipynb` | Figure 1 (precipitation) |
| `Fig1_generate_significance_masks.py` | Significance masks for Figure 1 |
| `Fig2_debm_SMB.ipynb` | Figure 2 (surface mass balance) |
| `Fig3_and_Tabs.m` | Figure 3 and tables |
| `FigS2_*.ipynb` | Supplementary Figure S2 |
| `PL2023_figS3_S6.m` | Supplementary Figures S3-S6 |
| `FigS7.m` | Supplementary Figure S7 |

## Citation

If you use this code or data, please cite:

> Sijbrandij, L., Gierz, P., & Krebs-Kanzow, U. (2025). Proglacial lakes substantially modulate the surface mass balance of retreating ice sheets. *Geophysical Research Letters*.

## License

This project is licensed under the MIT License -- see [LICENSE](LICENSE) for details.
