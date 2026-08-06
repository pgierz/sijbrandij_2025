#!/usr/bin/env python
# coding: utf-8

# # Fig 1 – JJA 2m Temperature
# 
# **Improvements over original:**
# - All 6 panels combined into a single figure
# - One shared colorbar per colormap group (Spectral_r for absolute, coolwarm for anomalies)
# - Increased colorbar font sizes
# 
# Links:
# - https://matplotlib.org/stable/tutorials/colors/colormaps.html
# - https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html
# 

# In[2]:


import cartopy.util
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec


# In[34]:


# ============================================================
# Fig 1 – all 6 panels in one figure with shared colorbars
# ============================================================
# Colormap groups:
#   Spectral_r : panels 1 (Fig1_1, Europe REF13ka) and 4 (Fig1_4, NA REF13ka)
#   coolwarm   : panels 2,3,5,6 (anomalies)

# --------------- data paths ---------------
GLACL_path  = '../data/100ymean_alakeGLAC_temp2_JJA_2250_2349.nc'
PLAKE_path  = '../data/100ymean_plake_temp2_JJA_2250_2349.nc'
ALAKE_path  = '../data/100ymean_alake13ka_temp2_JJA_2250_2349.nc'
BC_path     = '../data/bc_plake_nhem5km.nc'
BCL_path    = '../data/TOPicemsk.15ka.nc'
PSIG_PL     = '../data/PL_SigMaskSM.nc'
PSIG_AL     = '../data/AL_SigMaskSM.nc'

GLACL_data = netcdf_dataset(GLACL_path)
PLAKE_data = netcdf_dataset(PLAKE_path)
ALAKE_data = netcdf_dataset(ALAKE_path)
BC_data    = netcdf_dataset(BC_path)
BCL_data   = netcdf_dataset(BCL_path)
PSIG_PL_data = netcdf_dataset(PSIG_PL)
PSIG_AL_data = netcdf_dataset(PSIG_AL)

# --------------- shared grid vars ---------------
lats  = GLACL_data.variables['lat'][:]
lons  = GLACL_data.variables['lon'][:]
glac  = BC_data.variables['GLAC'][:]
plake = BC_data.variables['PLAKE'][:]
lats5 = BC_data.variables['lat'][:]
lons5 = BC_data.variables['lon'][:]
slm   = BCL_data.variables['HDC'][0,:,:]
llats = BCL_data.variables['YLATGLOBP5'][:]
llons = BCL_data.variables['XLONGLOB1'][:]

# significance masks
vsigp_PL = PSIG_PL_data.variables['temp_maskJJA'][:,:]
vsigp_AL = PSIG_AL_data.variables['temp_maskJJA'][:,:]

# --------------- color / norm settings ---------------
CBAR_TICKSIZE  = 150   # colorbar tick label size
CBAR_LABELSIZE = 150  # colorbar axis label size
TITLE_FONTSIZE = 120

# Absolute temperature (Spectral_r)
abs_level_min = -15
abs_level_max = 24
abs_bounds    = np.linspace(abs_level_min, abs_level_max, 14)
abs_bounds2   = (-12, -6, 0, 6, 12, 18, 24)

abs_norm      = mcolors.BoundaryNorm(boundaries=abs_bounds, ncolors=256)
abs_cmap      = 'Spectral_r'

# Anomaly temperature (coolwarm)
anom_bounds = (-12, -8, -4, -2, -1, -0.5, 0, 0.5, 1, 2, 4, 8, 12)
anom_norm   = mcolors.BoundaryNorm(boundaries=anom_bounds, ncolors=256)
anom_cmap   = 'coolwarm'

season = 'JJA'

# --------------- helper: add boundaries ---------------
def add_boundaries(ax, add_plake=False):

    ax.contour(llons, llats, slm,
               transform=ccrs.PlateCarree(),
               levels=[0], colors='black', linewidths=5, linestyles=['-'])
    ax.contour(lons5, lats5, glac,
               transform=ccrs.PlateCarree(),
               levels=[0], colors='cyan', linewidths=20, linestyles=['-'])
    if add_plake:
        ax.contour(lons5, lats5, plake,
                   transform=ccrs.PlateCarree(),
                   levels=[0], colors='blue', linewidths=20, linestyles=['-'])
        ax.contour(lons5, lats5, glac,
                   transform=ccrs.PlateCarree(),
                   levels=[0], colors='cyan', linewidths=12, linestyles=['-'])


def add_sig_dots(ax, vsig):
    for idx, lon_val in enumerate(lons):
        for idy, lat_val in enumerate(lats):
            if vsig[idy, idx] == 0:
                ax.plot(lon_val, lat_val, 'kX', transform=ccrs.PlateCarree())

# --------------- build figure ---------------
# Layout: 2 rows × 3 cols of map axes + 2 shared colorbar rows
# We use GridSpec with extra rows for the two colorbars.
#   row 0-1: maps (Europe left col, NA right col)  — 3 rows of maps
#   row 3: shared colorbar for Spectral_r (absolute)
#   row 4: shared colorbar for coolwarm   (anomalies)

fig = plt.figure(figsize=(100, 60))
gs  = GridSpec(3, 3, figure=fig,
               hspace=0.1, wspace=0.05,
               height_ratios=[1, 1, 0.06],
               width_ratios=[1, 1, 1])

eu_extent = [0,   40,  52, 73]
na_extent = [-115, -60, 35, 80]
proj_eu   = ccrs.NearsidePerspective(central_longitude=20,  central_latitude=60, satellite_height=700_000)
proj_eu_w = ccrs.NearsidePerspective(central_longitude=-90, central_latitude=60, satellite_height=700_000)
proj_na   = ccrs.NearsidePerspective(central_longitude=-90, central_latitude=60, satellite_height=10_000_000)
proj_eu_g = ccrs.NearsidePerspective(central_longitude=20,  central_latitude=60, satellite_height=10_000_000)

# ---- Row 0: REF13ka absolute (panels 1 & 4) ----
ax1 = fig.add_subplot(gs[0, 0], projection=proj_eu)
ax4 = fig.add_subplot(gs[1, 0], projection=proj_na)

for ax, ext, proj in [(ax1, eu_extent, proj_eu), (ax4, na_extent, proj_na)]:
    ax.set_extent(ext)
    varg = GLACL_data.variables['temp2'][0,:,:] - 273.15
    im_abs = ax.pcolormesh(lons, lats, varg,
                           transform=ccrs.PlateCarree(),
                           norm=abs_norm, cmap=abs_cmap)
    add_boundaries(ax, add_plake=False)

ax1.set_title(' REF13ka\n', fontsize=TITLE_FONTSIZE)
#ax4.set_title(' REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)

# ---- Row 1: PL13ka_warm anomaly (panels 2 & 5 — alake13ka) ----
ax2 = fig.add_subplot(gs[0, 1], projection=proj_eu)
ax5 = fig.add_subplot(gs[1, 1], projection=proj_na)

varg = GLACL_data.variables['temp2'][0,:,:]
varp_al = ALAKE_data.variables['temp2'][0,:,:]
for ax, ext in [(ax2, eu_extent), (ax5, na_extent)]:
    ax.set_extent(ext)
    im_anom = ax.pcolormesh(lons, lats, varp_al - varg,
                             transform=ccrs.PlateCarree(),
                             norm=anom_norm, cmap=anom_cmap,
                             alpha=0.7, edgecolor='none')
    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_AL)

ax2.set_title(' PL13ka - REF13ka\n', fontsize=TITLE_FONTSIZE)
#ax5.set_title(' PL13ka - REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)

# ---- Row 2: PL13ka anomaly (panels 3 & 6 — plake) ----
ax3 = fig.add_subplot(gs[0, 2], projection=proj_eu)
ax6 = fig.add_subplot(gs[1, 2], projection=proj_na)

varp_pl = PLAKE_data.variables['temp2'][0,:,:]
for ax, ext in [(ax3, eu_extent), (ax6, na_extent)]:
    ax.set_extent(ext)
    ax.pcolormesh(lons, lats, varp_pl - varg,
                  transform=ccrs.PlateCarree(),
                  norm=anom_norm, cmap=anom_cmap,
                  alpha=0.7, edgecolor='none')
    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_PL)

ax3.set_title(' PL13ka$_{cold}$ - REF13ka \n', fontsize=TITLE_FONTSIZE)
#ax6.set_title(' PL13ka$_{cold}$ - REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)



# ---- Shared colorbar row: anomaly (coolwarm) ----
cax_anom = fig.add_subplot(gs[2, 1:3])   # span columns 1 and 2
cbar_anom = fig.colorbar(im_anom, cax=cax_anom,
                         orientation='horizontal',
                         extend='both',
                         boundaries=anom_bounds,
                         ticks=anom_bounds,
                        )
cbar_anom.ax.tick_params(labelsize=CBAR_TICKSIZE)
cbar_anom.set_label('\n' + season + ' 2m temperature anomaly (°C)',
                    fontsize=CBAR_LABELSIZE)
cbar_anom.set_ticks(list(anom_bounds))
cbar_anom.set_ticklabels( [ '-12', '-8', '-4', '-2', '-1', '-0.5', '0', '0.5', '1', '2', '4', '8', '12'] )    
cax_abs = fig.add_subplot(gs[2, 0])
cbar_abs = fig.colorbar(im_abs, cax=cax_abs,
                        orientation='horizontal',
                        extend='both',
                        boundaries=abs_bounds)

cbar_abs.ax.tick_params(labelsize=CBAR_TICKSIZE,
                        length=25,
                        width=5
                       )
cbar_abs.set_label('\n T$_{2m}$, JJA (°C)', fontsize=CBAR_LABELSIZE)
cbar_abs.set_ticks(list(abs_bounds2))


cbar_anom.ax.tick_params(
    labelsize=CBAR_TICKSIZE,
    length=25,      # tick length
    width=5         # tick width
)

cbar_anom.ax.tick_params(labelsize=CBAR_TICKSIZE)
cbar_anom.set_label('\n $\Delta$ T$_{2m}$,  ' + season + '(°C)', fontsize=CBAR_LABELSIZE)
cbar_anom.set_ticks(list(anom_bounds))

fig.savefig('../FIGS/Fig1_combined.png', bbox_inches='tight', dpi=150)
plt.show()
print("Saved Fig1_combined.png")


# In[34]:


# ============================================================
# Fig 1 – all 6 panels in one figure with shared colorbars
# ============================================================
# Colormap groups:
#   Spectral_r : panels 1 (Fig1_1, Europe REF13ka) and 4 (Fig1_4, NA REF13ka)
#   coolwarm   : panels 2,3,5,6 (anomalies)

# --------------- data paths ---------------
GLACL_path  = '../data/100ymean_alakeGLAC_temp2_JJA_2250_2349.nc'
PLAKE_path  = '../data/100ymean_plake_temp2_JJA_2250_2349.nc'
ALAKE_path  = '../data/100ymean_alake13ka_temp2_JJA_2250_2349.nc'
BC_path     = '../data/bc_plake_nhem5km.nc'
BCL_path    = '../data/TOPicemsk.15ka.nc'
PSIG_PL     = '../data/PL_SigMaskSM.nc'
PSIG_AL     = '../data/AL_SigMaskSM.nc'

GLACL_data = netcdf_dataset(GLACL_path)
PLAKE_data = netcdf_dataset(PLAKE_path)
ALAKE_data = netcdf_dataset(ALAKE_path)
BC_data    = netcdf_dataset(BC_path)
BCL_data   = netcdf_dataset(BCL_path)
PSIG_PL_data = netcdf_dataset(PSIG_PL)
PSIG_AL_data = netcdf_dataset(PSIG_AL)

# --------------- shared grid vars ---------------
lats  = GLACL_data.variables['lat'][:]
lons  = GLACL_data.variables['lon'][:]
glac  = BC_data.variables['GLAC'][:]
plake = BC_data.variables['PLAKE'][:]
lats5 = BC_data.variables['lat'][:]
lons5 = BC_data.variables['lon'][:]
slm   = BCL_data.variables['HDC'][0,:,:]
llats = BCL_data.variables['YLATGLOBP5'][:]
llons = BCL_data.variables['XLONGLOB1'][:]

# significance masks
vsigp_PL = PSIG_PL_data.variables['temp_maskJJA'][:,:]
vsigp_AL = PSIG_AL_data.variables['temp_maskJJA'][:,:]

# --------------- color / norm settings ---------------
CBAR_TICKSIZE  = 150   # colorbar tick label size
CBAR_LABELSIZE = 150  # colorbar axis label size
TITLE_FONTSIZE = 120

# Absolute temperature (Spectral_r)
abs_level_min = -15
abs_level_max = 24
abs_bounds    = np.linspace(abs_level_min, abs_level_max, 14)
abs_bounds2   = (-12, -6, 0, 6, 12, 18, 24)

abs_norm      = mcolors.BoundaryNorm(boundaries=abs_bounds, ncolors=256)
abs_cmap      = 'Spectral_r'

# Anomaly temperature (coolwarm)
anom_bounds = (-12, -8, -4, -2, -1, -0.5, 0, 0.5, 1, 2, 4, 8, 12)
anom_norm   = mcolors.BoundaryNorm(boundaries=anom_bounds, ncolors=256)
anom_cmap   = 'coolwarm'

season = 'JJA'

# --------------- helper: add boundaries ---------------
def add_boundaries(ax, add_plake=False):

    ax.contour(llons, llats, slm,
               transform=ccrs.PlateCarree(),
               levels=[0], colors='black', linewidths=5, linestyles=['-'])
    ax.contour(lons5, lats5, glac,
               transform=ccrs.PlateCarree(),
               levels=[0], colors='cyan', linewidths=20, linestyles=['-'])
    if add_plake:
        ax.contour(lons5, lats5, plake,
                   transform=ccrs.PlateCarree(),
                   levels=[0], colors='blue', linewidths=20, linestyles=['-'])
        ax.contour(lons5, lats5, glac,
                   transform=ccrs.PlateCarree(),
                   levels=[0], colors='cyan', linewidths=12, linestyles=['-'])


def add_sig_dots(ax, vsig):
    for idx, lon_val in enumerate(lons):
        for idy, lat_val in enumerate(lats):
            if vsig[idy, idx] == 0:
                ax.plot(lon_val, lat_val, 'kX', transform=ccrs.PlateCarree())

# --------------- build figure ---------------
# Layout: 2 rows × 3 cols of map axes + 2 shared colorbar rows
# We use GridSpec with extra rows for the two colorbars.
#   row 0-1: maps (Europe left col, NA right col)  — 3 rows of maps
#   row 3: shared colorbar for Spectral_r (absolute)
#   row 4: shared colorbar for coolwarm   (anomalies)

fig = plt.figure(figsize=(100, 60))
gs  = GridSpec(3, 3, figure=fig,
               hspace=0.1, wspace=0.05,
               height_ratios=[1, 1, 0.06],
               width_ratios=[1, 1, 1])

eu_extent = [0,   40,  52, 73]
na_extent = [-115, -60, 35, 80]
proj_eu   = ccrs.NearsidePerspective(central_longitude=20,  central_latitude=60, satellite_height=700_000)
proj_eu_w = ccrs.NearsidePerspective(central_longitude=-90, central_latitude=60, satellite_height=700_000)
proj_na   = ccrs.NearsidePerspective(central_longitude=-90, central_latitude=60, satellite_height=10_000_000)
proj_eu_g = ccrs.NearsidePerspective(central_longitude=20,  central_latitude=60, satellite_height=10_000_000)

# ---- Row 0: REF13ka absolute (panels 1 & 4) ----
ax1 = fig.add_subplot(gs[0, 0], projection=proj_eu)
ax4 = fig.add_subplot(gs[1, 0], projection=proj_na)

for ax, ext, proj in [(ax1, eu_extent, proj_eu), (ax4, na_extent, proj_na)]:
    ax.set_extent(ext)
    varg = GLACL_data.variables['temp2'][0,:,:] - 273.15
    im_abs = ax.pcolormesh(lons, lats, varg,
                           transform=ccrs.PlateCarree(),
                           norm=abs_norm, cmap=abs_cmap)
    add_boundaries(ax, add_plake=False)

ax1.set_title(' REF13ka\n', fontsize=TITLE_FONTSIZE)
#ax4.set_title(' REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)

# ---- Row 1: PL13ka_warm anomaly (panels 2 & 5 — alake13ka) ----
ax2 = fig.add_subplot(gs[0, 1], projection=proj_eu)
ax5 = fig.add_subplot(gs[1, 1], projection=proj_na)

varg = GLACL_data.variables['temp2'][0,:,:]
varp_al = ALAKE_data.variables['temp2'][0,:,:]
for ax, ext in [(ax2, eu_extent), (ax5, na_extent)]:
    ax.set_extent(ext)
    im_anom = ax.pcolormesh(lons, lats, varp_al - varg,
                             transform=ccrs.PlateCarree(),
                             norm=anom_norm, cmap=anom_cmap,
                             alpha=0.7, edgecolor='none')
    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_AL)

ax2.set_title(' PL13ka - REF13ka\n', fontsize=TITLE_FONTSIZE)
#ax5.set_title(' PL13ka - REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)

# ---- Row 2: PL13ka anomaly (panels 3 & 6 — plake) ----
ax3 = fig.add_subplot(gs[0, 2], projection=proj_eu)
ax6 = fig.add_subplot(gs[1, 2], projection=proj_na)

varp_pl = PLAKE_data.variables['temp2'][0,:,:]
for ax, ext in [(ax3, eu_extent), (ax6, na_extent)]:
    ax.set_extent(ext)
    ax.pcolormesh(lons, lats, varp_pl - varg,
                  transform=ccrs.PlateCarree(),
                  norm=anom_norm, cmap=anom_cmap,
                  alpha=0.7, edgecolor='none')
    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_PL)

ax3.set_title(' PL13ka$_{cold}$ - REF13ka \n', fontsize=TITLE_FONTSIZE)
#ax6.set_title(' PL13ka$_{cold}$ - REF13ka (N. America)\n', fontsize=TITLE_FONTSIZE)



# ---- Shared colorbar row: anomaly (coolwarm) ----
cax_anom = fig.add_subplot(gs[2, 1:3])   # span columns 1 and 2
cbar_anom = fig.colorbar(im_anom, cax=cax_anom,
                         orientation='horizontal',
                         extend='both',
                         boundaries=anom_bounds,
                         ticks=anom_bounds,
                        )
cbar_anom.ax.tick_params(labelsize=CBAR_TICKSIZE)
cbar_anom.set_label('\n' + season + ' 2m temperature anomaly (°C)',
                    fontsize=CBAR_LABELSIZE)
cbar_anom.set_ticks(list(anom_bounds))
cbar_anom.set_ticklabels( [ '-12', '-8', '-4', '-2', '-1', '-0.5', '0', '0.5', '1', '2', '4', '8', '12'] )    
cax_abs = fig.add_subplot(gs[2, 0])
cbar_abs = fig.colorbar(im_abs, cax=cax_abs,
                        orientation='horizontal',
                        extend='both',
                        boundaries=abs_bounds)

cbar_abs.ax.tick_params(labelsize=CBAR_TICKSIZE,
                        length=25,
                        width=5
                       )
cbar_abs.set_label('\n T$_{2m}$, JJA (°C)', fontsize=CBAR_LABELSIZE)
cbar_abs.set_ticks(list(abs_bounds2))


cbar_anom.ax.tick_params(
    labelsize=CBAR_TICKSIZE,
    length=25,      # tick length
    width=5         # tick width
)

cbar_anom.ax.tick_params(labelsize=CBAR_TICKSIZE)
cbar_anom.set_label('\n $\Delta$ T$_{2m}$,  ' + season + '(°C)', fontsize=CBAR_LABELSIZE)
cbar_anom.set_ticks(list(anom_bounds))

fig.savefig('../FIGS/Fig1_combined.png', bbox_inches='tight', dpi=150)
plt.show()
print("Saved Fig1_combined.png")


# In[ ]:




