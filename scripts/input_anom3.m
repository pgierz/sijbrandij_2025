function [cbh,figh]=smb_anom(anom1, anom2, anom3, lev2,map,clabel,figname)
gmsk=ncread('~/wrkpal/lianne/processed_output/GLAC1D_on_nhem5km_4debm.nc','GLAC');
topo=ncread('~/wrkpal/lianne/processed_output/GLAC1D_on_nhem5km_4debm.nc','TOPO');
pmsk=ncread('~/wrkpal/lianne/processed_output/pmask5km.nc','PLAKE');
if (nargin==1)
fig=1;
end
if (nargin<3)
	keyboard
minv=nanumin(anom(:));
maxv=nanumax(anom(:));
figtit=[]
end


map_yr   = dlmread('~/matlab/colormaps/cmocean_matter.rgb')/256;%MPL_virdis.rgb');
map_gb   = dlmread('~/matlab/colormaps/cmocean_deep.rgb')/256;%MPL_virdis.rgb');
map_wygb = dlmread('~/matlab/colormaps/WBGYR.rgb')/256;   %MPL_virdis.rgb');
map_test  = dlmread('~/matlab/colormaps/ocean_ice.rgb')/256;
map_gb=map_gb(end:-1:10,:);
map1=map_test(end:-1:1);
map2=map_gb;
figure
clf
hold
tiledlayout(1,3,"TileSpacing","compact","Padding","compact")
nexttile
hold
[cbh,figh]=pcolor_nl(anom1',lev2,map)
caxis([1 length(lev2)])
contour(topo',[1 1],'Color',[.6 .6 .6],'Linewidth',.2);
contour(topo'.*gmsk',[1000 2000 3000],'Color',[.7 .7 .7],'Linewidth',.2);
contour(gmsk',[.1 .1],'k','Linewidth',.2);
set(gca,'XTick',[],'YTick',[]);
shading flat
box on
colorbar off
set(gca,'XTick',[],'YTick',[]);
axis image
axis tight
text(min(xlim), max(ylim), sprintf(' a'), 'Horiz','left', 'Vert','top')
contour(pmsk',[1 1],'c','LineWidth',.2);
nexttile

hold
[cbh,figh]=pcolor_nl(anom2',lev2,map)
caxis([1 length(lev2)])
contour(topo',[1 1],'Color',[.6 .6 .6],'Linewidth',.2);
contour(topo'.*gmsk',[1000 2000 3000],'Color',[.7 .7 .7],'Linewidth',.2);
contour(gmsk',[.1 .1],'k','Linewidth',1);
set(gca,'XTick',[],'YTick',[]);
shading flat
box on

text(min(xlim), max(ylim), sprintf(' b'), 'Horiz','left', 'Vert','top')
set(gca,'XTick',[],'YTick',[]);
axis image
axis tight
contour(pmsk',[1 1],'c','LineWidth',.2);
colorbar off
nexttile
hold
[cbh,figh]=pcolor_nl(anom3',lev2,map)
caxis([1 length(lev2)])
contour(topo',[1 1],'Color',[.6 .6 .6],'Linewidth',.2);
contour(topo'.*gmsk',[1000 2000 3000],'Color',[.7 .7 .7],'Linewidth',.2);
contour(gmsk',[.1 .1],'k','Linewidth',.2);
set(gca,'XTick',[],'YTick',[]);
shading flat
box on
text(min(xlim), max(ylim), sprintf(' c'), 'Horiz','left', 'Vert','top')
%set(cbh,'Position', [0.1 0.46 0.8 0.05], 'Orientation', 'horizontal');
cbh.Layout.Tile = 'South';
xlabel(cbh,clabel) 
set(gca,'XTick',[],'YTick',[]);
axis image
axis tight
contour(pmsk',[1 1],'c','LineWidth',.2);

figh=gcf;
set(gcf,'GraphicsSmoothing','off')
if (nargin==7)
    exportgraphics(gcf, figname , 'ContentType', 'vector')
end
