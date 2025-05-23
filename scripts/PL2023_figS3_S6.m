% The directory suppdata is very large but availale upon request, please contact ukrebska@awi.de
clear all
close all
addpath('~/matlab/dEBM/figures');
addpath('~/matlab/dEBM_AWIxM');
map_yr   = dlmread('~/matlab/colormaps/cmocean_matter.rgb')/256;%MPL_virdis.rgb');
map_gb   = dlmread('~/matlab/colormaps/cmocean_deep.rgb')/256;%MPL_virdis.rgb');
map_wygb = dlmread('~/matlab/colormaps/WBGYR.rgb')/256;   %MPL_virdis.rgb');
map_test  = dlmread('~/matlab/colormaps/ocean_ice.rgb')/256;
map_gb=map_gb(end:-1:10,:);
map1=map_test(end:-1:1);
map2=map_gb;
topo=ncread('../suppdata/topo5km.nc','TOPO');
pp=ncread('../suppdata/ANOM_YM_PL13ka5km.nc','aprt')*365*86400/1000;
pp_seas=ncread('../suppdata/ANOM_PL13ka5km.nc','aprt')*365*86400/1000;
t2m=ncread('../suppdata/ANOM_PL13ka5km.nc','temp2');
ppw=ncread('../suppdata/ANOM_YM_PLwarm13ka5km.nc','aprt')*365*86400/1000;
ppw_seas=ncread('../suppdata/ANOM_PLwarm13ka5km.nc','aprt')*365*86400/1000;
t2mw=ncread('../suppdata/ANOM_PLwarm13ka5km.nc','temp2');
t2mPL=ncread('../suppdata/ANOM_PL_PLwarm13ka5km.nc','temp2');
ppPL=ncread('../suppdata/ANOM_YM_PL_PLwarm13ka5km.nc','aprt')*365*86400/1000;
ppPL_seas=ncread('../suppdata/ANOM_PL_PLwarm13ka5km.nc','aprt')*365*86400/1000;
smsk_t_DJFap=ncread('../suppdata/ALPL_SigMaskSM5km.nc','temp_maskDJF')+1;
smsk_t_JJAap=ncread('../suppdata/ALPL_SigMaskSM5km.nc','temp_maskJJA')+1;
smsk_pap=ncread('../suppdata/ALPL_SigMaskSM5km.nc','prcip_mask')+1;
smsk_papDJF=ncread('../suppdata/ALPL_SigMaskSM5km.nc','prcip_maskDJF')+1;
smsk_papJJA=ncread('../suppdata/ALPL_SigMaskSM5km.nc','prcip_maskJJA')+1;
smsk_t_DJFa=ncread('../suppdata/AL_SigMaskSM5km.nc','temp_maskDJF')+1;
smsk_t_JJAa=ncread('../suppdata/AL_SigMaskSM5km.nc','temp_maskJJA')+1;
smsk_pa=ncread('../suppdata/AL_SigMaskSM5km.nc','prcip_mask')+1;
smsk_paDJF=ncread('../suppdata/AL_SigMaskSM5km.nc','prcip_maskDJF')+1;
smsk_paJJA=ncread('../suppdata/AL_SigMaskSM5km.nc','prcip_maskJJA')+1;
smsk_t_DJF=ncread('../suppdata/PL_SigMaskSM5km.nc','temp_maskDJF')+1;
smsk_t_JJA=ncread('../suppdata/PL_SigMaskSM5km.nc','temp_maskJJA')+1;
smsk_p=ncread('../suppdata/PL_SigMaskSM5km.nc','prcip_mask')+1;
smsk_pDJF=ncread('../suppdata/PL_SigMaskSM5km.nc','prcip_maskDJF')+1;
smsk_pJJA=ncread('../suppdata/PL_SigMaskSM5km.nc','prcip_maskJJA')+1;
lev2=[-15 -10 -5 -2 -1 -0.5 -.25 0 .25 .5 1 2 5 10 15]
[map,lev]=create_anom_map_from2maps(-length(find(lev2<0)), length(find(lev2>0)),length(lev2),map_test,map_yr);
anom1=mean(t2m(:,:, [6 7 8]),3).*smsk_t_JJA;
anom2=mean(t2mw(:,:, [6 7 8]),3).*smsk_t_JJAa;
anom3=mean(t2mPL(:,:,[6 7 8]),3).*smsk_t_JJAap;
%figtit={'T2m (JJA, PL13ka-REF13ka)';'T2m (JJA, PL13ka_{warm}-REF13ka)';'T2m (JJA, PL13ka-PL13ka_{warm})'}
clabel='\Delta T2M (K)';
[cbh,h1]=input_anom3(anom1,anom2,anom3,lev2,map,clabel)
exportgraphics(h1, '~/paper/Sijbrandij_2023/rev1/data_and_scripts/LSijbrandij_2023/supp_figures//S5.pdf' , 'ContentType', 'image')
anom1=mean(t2m(:,:, [12 1 2]),3).*smsk_t_DJF;
anom2=mean(t2mw(:,:, [12 1 2]),3).*smsk_t_DJFa;
anom3=mean(t2mPL(:,:,[12 1 2]),3).*smsk_t_DJFap;
[cbh,h1]=input_anom3(anom1,anom2,anom3,lev2,map,clabel)
exportgraphics(h1, '~/paper/Sijbrandij_2023/rev1/data_and_scripts/LSijbrandij_2023/supp_figures//S6.pdf' , 'ContentType', 'image')
clabel='\Delta precip (m/yr)'
lev2=[-.5 -.3 -.15 -.1 -.075 -.05 -0.025 0 .025 .05 .075 .1 .15 .3 .5]
[map,lev]=create_anom_map_from2maps(-length(find(lev<0)), length(find(lev>0)),length(lev),map_test,map_yr);
anom1=mean(pp_seas(:,:,6:8),3).*smsk_pJJA;;
anom2=mean(ppw_seas(:,:,6:8),3).*smsk_paJJA;;
anom3=mean(ppPL_seas(:,:,6:8),3).*smsk_papJJA;
[cbh,h1]=input_anom3(anom1,anom2,anom3,lev2,map,clabel)
exportgraphics(h1, '~/paper/Sijbrandij_2023/rev1/data_and_scripts/LSijbrandij_2023/supp_figures//S3.pdf' , 'ContentType', 'image')
anom1=mean(pp_seas(:,:,[12 1 2]),3).*smsk_pDJF;
anom2=mean(ppw_seas(:,:,[12 1 2]),3).*smsk_paDJF;
anom3=mean(ppPL_seas(:,:,[12 1 2]),3).*smsk_papDJF;
[cbh,h1]=input_anom3(anom1,anom2,anom3,lev2,map,clabel)
exportgraphics(h1, '~/paper/Sijbrandij_2023/rev1/data_and_scripts/LSijbrandij_2023/supp_figures//S4.pdf' , 'ContentType', 'image')
