#!/usr/bin/env python
# coding: utf-8

# # Fig 2 – Annual Total Precipitation
# 
# **Improvements over original:**
# - All 6 panels combined into a single figure
# - One shared colorbar per colormap group (GnBu for absolute, RdBu for anomalies)
# - Increased colorbar font sizes
# 

# In[30]:


import cartopy.util
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import cmocean.cm as cmo
from matplotlib.gridspec import GridSpec


# In[31]:


# ============================================================
# Fig 2 – combined precipitation figure
# ============================================================

GLACL_path  = '../data/100ymean_alakeGLAC_precip_ym_2250_2349.nc'
ALAKE_path  = '../data/100ymean_alake13ka_precip_ym_2250_2349.nc'
PLAKE_path  = '../data/100ymean_plake_precip_ym_2250_2349.nc'

BC_path     = '../data/bc_plake_nhem5km.nc'
BCL_path    = '../data/TOPicemsk.15ka.nc'

PSIG_AL     = '../data/AL_SigMaskSM.nc'
PSIG_PL     = '../data/PL_SigMaskSM.nc'

GLACL_data = netcdf_dataset(GLACL_path)
ALAKE_data = netcdf_dataset(ALAKE_path)
PLAKE_data = netcdf_dataset(PLAKE_path)

BC_data    = netcdf_dataset(BC_path)
BCL_data   = netcdf_dataset(BCL_path)

PSIG_AL_data = netcdf_dataset(PSIG_AL)
PSIG_PL_data = netcdf_dataset(PSIG_PL)


# In[32]:


lats  = GLACL_data.variables['lat'][:]
lons  = GLACL_data.variables['lon'][:]

glac  = BC_data.variables['GLAC'][:]
plake = BC_data.variables['PLAKE'][:]

lats5 = BC_data.variables['lat'][:]
lons5 = BC_data.variables['lon'][:]

slm   = BCL_data.variables['HDC'][0,:,:]
llats = BCL_data.variables['YLATGLOBP5'][:]
llons = BCL_data.variables['XLONGLOB1'][:]

vsigp_AL = PSIG_AL_data.variables['prcip_mask'][:,:]
vsigp_PL = PSIG_PL_data.variables['prcip_mask'][:,:]


# In[33]:


CBAR_TICKSIZE  = 150
CBAR_LABELSIZE = 150
TITLE_FONTSIZE = 120


# In[34]:


abs_bounds = np.linspace(0,1200,25)
abs_norm   = mcolors.BoundaryNorm(abs_bounds, 256)
abs_cmap   = "GnBu"

anom_bounds = (
    -175,-125,-75,-50,-25,
    -10,0,
    10,25,50,75,125,175
)

anom_norm = mcolors.BoundaryNorm(anom_bounds,256)
anom_cmap = "RdBu"


# In[35]:


def add_boundaries(ax, add_plake=False):

    ax.contour(
        llons,llats,slm,
        transform=ccrs.PlateCarree(),
        levels=[0],
        colors='black',
        linewidths=5
    )

    ax.contour(
        lons5,lats5,glac,
        transform=ccrs.PlateCarree(),
        levels=[0],
        colors='cyan',
        linewidths=20
    )

    if add_plake:
        ax.contour(
            lons5,lats5,plake,
            transform=ccrs.PlateCarree(),
            levels=[0],
            colors='blue',
            linewidths=20
        )

        ax.contour(
            lons5,lats5,glac,
            transform=ccrs.PlateCarree(),
            levels=[0],
            colors='cyan',
            linewidths=12
        )


# In[ ]:





# In[36]:


def add_sig_dots(ax, vsig):

    for idx, lon_val in enumerate(lons):
        for idy, lat_val in enumerate(lats):

            if vsig[idy, idx] == 0:
                ax.plot(
                    lon_val,
                    lat_val,
                    'kX',
                    transform=ccrs.PlateCarree()
                )


# In[37]:


fig = plt.figure(figsize=(100,60))

gs = GridSpec(
    3,3,
    figure=fig,
    hspace=0.1,
    wspace=0.05,
    height_ratios=[1,1,0.06]
)


# In[38]:


eu_extent = [0,40,52,73]
na_extent = [-115,-60,35,80]

proj_eu = ccrs.NearsidePerspective(
    central_longitude=20,
    central_latitude=60,
    satellite_height=700_000
)

proj_na = ccrs.NearsidePerspective(
    central_longitude=-90,
    central_latitude=60,
    satellite_height=10_000_000
)


# In[39]:


varg = GLACL_data.variables['precip'][0,:,:]

ax1 = fig.add_subplot(gs[0,0], projection=proj_eu)
ax4 = fig.add_subplot(gs[1,0], projection=proj_na)

for ax,ext in [(ax1,eu_extent),(ax4,na_extent)]:

    ax.set_extent(ext)

    im_abs = ax.pcolormesh(
        lons,lats,varg,
        transform=ccrs.PlateCarree(),
        norm=abs_norm,
        cmap=abs_cmap
    )

    add_boundaries(ax)

ax1.set_title('REF13ka\n', fontsize=TITLE_FONTSIZE)


# In[40]:


ax2 = fig.add_subplot(gs[0,1], projection=proj_eu)
ax5 = fig.add_subplot(gs[1,1], projection=proj_na)

varp_al = ALAKE_data.variables['precip'][0,:,:]

for ax,ext in [(ax2,eu_extent),(ax5,na_extent)]:

    ax.set_extent(ext)

    im_anom = ax.pcolormesh(
        lons,lats,
        varp_al-varg,
        transform=ccrs.PlateCarree(),
        norm=anom_norm,
        cmap=anom_cmap,
        alpha=0.7
    )

    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_AL)

ax2.set_title(
    'PL13ka - REF13ka\n',
    fontsize=TITLE_FONTSIZE
)


# In[41]:


ax3 = fig.add_subplot(gs[0,2], projection=proj_eu)
ax6 = fig.add_subplot(gs[1,2], projection=proj_na)

varp_pl = PLAKE_data.variables['precip'][0,:,:]

for ax,ext in [(ax3,eu_extent),(ax6,na_extent)]:

    ax.set_extent(ext)

    ax.pcolormesh(
        lons,lats,
        varp_pl-varg,
        transform=ccrs.PlateCarree(),
        norm=anom_norm,
        cmap=anom_cmap,
        alpha=0.7
    )

    add_boundaries(ax, add_plake=True)
    add_sig_dots(ax, vsigp_PL)

ax3.set_title(
    'PL13ka$_{cold}$ - REF13ka\n',
    fontsize=TITLE_FONTSIZE
)


# In[42]:


cax_abs = fig.add_subplot(gs[2,0])

cbar_abs = fig.colorbar(
    im_abs,
    cax=cax_abs,
    orientation='horizontal',
    extend='max'
)

cbar_abs.ax.tick_params(
    labelsize=CBAR_TICKSIZE,
    length=25,
    width=5
)

cbar_abs.set_label(
    '\n Total precipitation (mm yr$^{-1}$)',
    fontsize=CBAR_LABELSIZE
)


# In[43]:


cax_anom = fig.add_subplot(gs[2,1:3])

cbar_anom = fig.colorbar(
    im_anom,
    cax=cax_anom,
    orientation='horizontal',
    extend='both'
)

cbar_anom.ax.tick_params(
    labelsize=CBAR_TICKSIZE,
    length=25,
    width=5
)

cbar_anom.set_label(
    '\n Δ precipitation (mm yr$^{-1}$)',
    fontsize=CBAR_LABELSIZE
)


# In[44]:


fig.savefig(
    '../FIGS/Fig2_combined.png',
#    bbox_inches='tight',
#    dpi=150
#)

#plt.show()

print("Saved Fig2_combined.png")


# In[45]:


plt.show()


# In[ ]:




