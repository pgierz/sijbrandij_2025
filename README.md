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
├── FIGS/             # Output directory for notebook-generated figures
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

Model output data (~18 GB) is archived on Zenodo. Download with:

```bash
./download-data.sh
```

**Note:** On Binder, the data download takes approximately 15-20 minutes. Please be patient while the download completes before running the notebooks.

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
| `Fig1_echam_T2m.ipynb` | Figure 1_1, 1_2 .. 1_6 (temperature) |
| `Fig2_echam_precip.ipynb` | Figure 2_1, 2_2,..2_6 (precipitation) |
| `Fig1_2_generate_significance_masks.py` | Significance masks for Figures 1&2 |
| `Fig3_debm_SMB.ipynb` | Figure 3_1, 3_2, .. 3_6 (surface mass balance) |
| `Fig4_and_Tabs.m` | Figure 4_1, 4_2, 4_3 and all tables (article and Suppl.)  |
| `FigS2_5.m` | Supplementary Figures S2..S5 |
| `FigS7S8_lakemodel.m` | Lake model and Supplementary Figures S7&S8 |
| `input_anom3.m` | called by FigS2_5.m |
| `PDD4.m` | called by Fig4.m |


## Citation

If you use this code or data, please cite:

>Lianne Sijbrandij, Uta Krebs-Kanzow, Paul Gierz, et al. Proglacial lakes substantially modulate the surface mass balance of deglacial ice sheets. ESS Open Archive . February 06, 2026.
DOI: 10.22541/essoar.174861028.86292675/v2 
and
Gierz, P., Sijbrandij, L., & Krebs-Kanzow, U. (2026). Proglacial lakes substantially modulate the surface mass balance of retreating ice sheets: Data (egusphere-2026-740) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18545093
## License

This project is licensed under the MIT License -- see [LICENSE](LICENSE) for details.
