# Proglacial lakes substantially modulate the surface mass balance of retreating ice sheets 
> Authors: Lianne Sijbrandij, Paul Gierz, Uta Krebs-Kanzow   

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pgierz/sijbrandij_2025/HEAD)

The `scripts` directory contains the scripts (jupyter notebooks, python3 and shell script making use of cdo) and
data which were used to generate the figures and tables in the main manuscript Sijbrandij et al. (2023 submitted to GRL).
Script names indicate which figures are produced. 

In these scripts we use the internal experiment names which differ from the manuscript:

| **Experiment ID** | **Internal Name** |
| ----------------- | ----------------- |
| `alakeGLAC`       | `REF13ka`         |
| `alake13ka`       | `PL13ka_{warm}`   | 
| `plake`           | `PL13ka`          |

For Fig1. Fig1_generate_significance_masks.py has analysed 100yr monthly mean atmosphere model output to generate
the masks which were used in Fig1 to highlight significant anomalies. All necessary input data are stored in 
directory data

## System Requirements

For Python and Jupyter notebooks please provide the following libraries:

matplotlib, numpy, netcdf4, cartopy, xarray, scipy

You can also use the supplied [`environment.yml`](./environment.yml):

```
$ conda env create
```
## Data Download
Data for this publication has been uploaded to Zenodo: [DOI](https://doi.org/10.5281/zenodo.15497082)

You can use the script to download the corresponding data:

```
$ ./download-data.sh
```
