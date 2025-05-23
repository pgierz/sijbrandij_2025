mskL=ncread('../data/mskLIS.nc','matrix');
mskL=mskL(:,:,ones(12,1));
mskF=ncread('../data/mskFIS.nc','matrix');
mskF=mskF(:,:,ones(12,1));
snPL=ncread('../data/ymonmean_plake_dEBM_out.nc','snow');
rnPL=ncread('../data/ymonmean_plake_dEBM_out.nc','rain');
tPL=ncread('../data/ymonmean_plake_for_dEBM.nc','air_temp');
sPLL=squeeze(nansum(nansum(snPL.*mskL,1),2));
rPLL=squeeze(nansum(nansum(rnPL.*mskL,1),2));
sPLF=squeeze(nansum(nansum(snPL.*mskF,1),2));
rPLF=squeeze(nansum(nansum(rnPL.*mskF,1),2));
tPLF=squeeze(nansum(nansum(tPL.*mskF,1),2))./squeeze(nansum(nansum(mskF,1),2));
tPLL=squeeze(nansum(nansum(tPL.*mskL,1),2))./squeeze(nansum(nansum(mskL,1),2));


snREF=ncread('../data/ymonmean_alakeGLAC_dEBM_out.nc','snow');
rnREF=ncread('../data/ymonmean_alakeGLAC_dEBM_out.nc','rain');
tREF=ncread('../data/ymonmean_alakeGLAC_for_dEBM.nc','air_temp');
sREFL=squeeze(nansum(nansum(snREF.*mskL,1),2));
rREFL=squeeze(nansum(nansum(rnREF.*mskL,1),2));
sREFF=squeeze(nansum(nansum(snREF.*mskF,1),2));
rREFF=squeeze(nansum(nansum(rnREF.*mskF,1),2));
tREFL=squeeze(nansum(nansum(tREF.*mskL,1),2))./squeeze(nansum(nansum(mskL,1),2));
tREFF=squeeze(nansum(nansum(tREF.*mskF,1),2))./squeeze(nansum(nansum(mskF,1),2));

snPL2=ncread('../data/ymonmean_alake13ka_dEBM_out.nc','snow');
rnPL2=ncread('../data/ymonmean_alake13ka_dEBM_out.nc','rain');
tPL2=ncread('../data/ymonmean_alake13ka_for_dEBM.nc','air_temp');

sPLL2=squeeze(nansum(nansum(snPL2.*mskL,1),2));
rPLL2=squeeze(nansum(nansum(rnPL2.*mskL,1),2));
sPLF2=squeeze(nansum(nansum(snPL2.*mskF,1),2));
rPLF2=squeeze(nansum(nansum(rnPL2.*mskF,1),2));
tPLL2=squeeze(nansum(nansum(tPL2.*mskL,1),2))./squeeze(nansum(nansum(mskL,1),2));
tPLF2=squeeze(nansum(nansum(tPL2.*mskF,1),2))./squeeze(nansum(nansum(mskF,1),2));

mthl=[31,28,31,30,31,30,31,31,30,31,30,31];
figure(1)
clf
hold
h1=plot((tREFF)','k-','LineWidth',2);
h2=plot((tPLF)','c-','LineWidth',2);
h3=plot((tPLF2)','r','LineWidth',2);

grid
legend([h1,h2,h3],{'REF13ka';'PL13ka';'PL13ka_{warm}'},'location','NorthWest')
xlabel('month')
xlim([1 12])
ylabel('2m Temperature ()')
title('FIS')
set(gca,'FontSize',14)
%exportgraphics(gcf,'../FIGS/temp_seasonalityFIS.pdf')

figure(2)
clf
hold
h1=plot((tREFL)','k-','LineWidth',2);
h2=plot((tPLL)','c-','LineWidth',2);
h3=plot((tPLL2)','r','LineWidth',2);

grid
legend([h1,h2,h3],{'REF13ka';'PL13ka';'PL13ka_{warm}'},'location','NorthWest')
xlabel('month')
xlim([1 12])
ylabel('2m Temperature ()')
title('NAIS')
set(gca,'FontSize',14)
%exportgraphics(gcf,'../FIGS/temp_seasonalityNAIS.pdf')

figure(3)
clf
hold
h1=plot((sREFF+rREFF).*mthl'.*25e6/1e12','k-','LineWidth',2);
h2=plot((sPLF+rPLF).*mthl'.*25e6/1e12','c-','LineWidth',2);
h3=plot((sPLF2+rPLF2).*mthl'.*25e6/1e12','r','LineWidth',2);
plot(sREFF.*mthl'.*25e6/1e12','k-.','LineWidth',2);
plot(sPLF.*mthl'.*25e6/1e12','c-.','LineWidth',2);
plot(sPLF2.*mthl'.*25e6/1e12','r-.','LineWidth',2);
plot(rREFF.*mthl'.*25e6/1e12','k:','LineWidth',2);
plot(rPLF.*mthl'.*25e6/1e12','c:','LineWidth',2);
plot(rPLF2.*mthl'.*25e6/1e12','r:','LineWidth',2);

grid
legend([h1,h2,h3],{'REF13ka';'PL13ka';'PL13ka_{warm}'},'location','NorthWest')
xlabel('month')
xlim([1 12])
ylabel('precipitation (Gt)')
title('FIS')
set(gca,'FontSize',14)
exportgraphics(gcf,'../supp_figures/S7_FIS.pdf')
figure(4)
clf
hold
h1=plot((sREFL+rREFL).*mthl'.*25e6/1e12','k-','LineWidth',2);
h2=plot((sPLL+rPLL).*mthl'.*25e6/1e12','c-','LineWidth',2);
h3=plot((sPLL2+rPLL2).*mthl'.*25e6/1e12','r','LineWidth',2);
plot(sREFL.*mthl'.*25e6/1e12','k-.','LineWidth',2);
plot(sPLL.*mthl'.*25e6/1e12','c-.','LineWidth',2);
plot(sPLL2.*mthl'.*25e6/1e12','r-.','LineWidth',2);
plot(rREFL.*mthl'.*25e6/1e12','k:','LineWidth',2);
plot(rPLL.*mthl'.*25e6/1e12','c:','LineWidth',2);
plot(rPLL2.*mthl'.*25e6/1e12','r:','LineWidth',2);

grid
legend([h1,h2,h3],{'REF13ka';'PL13ka';'PL13ka_{warm}'},'location','NorthWest')
xlabel('month')
xlim([1 12])
ylabel('precipitation (Gt)')
title('LIS')
set(gca,'FontSize',14)

exportgraphics(gcf,'../supp_figures/S7_LIS.pdf')

