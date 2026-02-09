figure(4)
clf
hold
exper='FIS'
tsurf_lm=zeros(365,2);
tsurf_cm=zeros(365,2);
Cexps={'PL13ka_{warm}','PL13ka'}
for proglacial=0:1


if proglacial 
  fname = ['../data/lake_surf_' exper '_plake.nc'] 
else
  fname = ['../data/lake_surf_' exper '_alake13ka.nc']
end



% Parameters
mths         = [31 31 28 31 30 31 30 31 31 30 31 30 31 31];  % 14 mthlengths Dec, Jan, ... Jan
mthse=cumsum(mths(2:end-1));
mths1=cumsum([1 mths(2:end-2)]);
midmonths    = cumsum(mths)-mths/2-31; % needed to interpolate from mthly to daily forcing  
nt           = 365                     % days per year
days         = 1:nt;
nyrs         = 250;
depth        = 300;                    % Depth of the lake in meters
dz           = 4;                      % depth / num_layers; % Thickness of each layer
mld          = 8;
num_layers   = depth/dz;               % Number of layers
dt           = 3600 * 24;              % Time step of one day in seconds
alpham       = 2e-5;                   % Thermal diffusivity of water in m^2/s in the mixed layer
alphad       = 5e-7;                   % Thermal diffusivity of water in m^2/s below mixed layer
rho_w        = 1000;                   % Density of water (kg/m^3)
c_pw         = 4186;                   % Specific heat capacity of water (J/kg·K)
L_i          = 334000;                 % Latent heat of fusion for ice (J/kg)
T_f          = 273.15;                 % Freezing point temperature (K)
if strcmp(exper,'NAIS')
h            = 30;                     % Heat transfer coefficient air/sea in W/m^2/°C (~5 - 30 W/m^2/K)
else
h            = 20;                     % Heat transfer coefficient air/sea in W/m^2/°C (~5 - 30 W/m^2/K)
end
emissivity_w = 0.97;                   % Emissivity of water
sigma        = 5.67e-8;                % Stefan-Boltzmann constant in W/m^2/K^4
alpha        = ((1:num_layers)*dz <= mld)*alpham+((1:num_layers)*dz > mld)*alphad;
%harmonic mean
alpha_if     =  2*(alpha(1:end-1).*alpha(2:end))./(alpha(1:end-1)+alpha(2:end))



% Read Forcing data: monthly mean 2m air temperature, incoming shortwave radiation, downward
% longwave radiation, and seaice cover from climate simulations 
% Read surface temperature as limit for experiment "PL13ka" and as
% reference for"PL13ka_warm"    

air_temp12 = ncread(fname,'temp2');                      
swd12      = ncread(fname,'swd');
lwd12      = ncread(fname,'lwd');
seaice12   = ncread(fname,'seaice');
tsurf12_cma    = ncread(fname,'tsurf');                           % skin temperature (lake or frozen lake)
tsurf12_cml= max(T_f,seaice12*T_f+(1-seaice12).*tsurf12_cma);     % estimated surface water temperature (beneath lake ice) 
% we assume that the parts of the lake surface which are ice covered are at melting point 
air_temp12ow = max(T_f,(air_temp12-seaice12*T_f)./(1-seaice12));  % estimated air temperature above open water  
air_temp12ow(find(seaice12>0.95))=T_f;
% interpolate forcing data to daily resolution
Tair       = spline(midmonths,air_temp12ow([12 1:12 1]),days);
swd        = spline(midmonths,swd12([12 1:12 1]),days);
lwd        = spline(midmonths,lwd12([12 1:12 1]),days);
seaice     = (max(0,min(1,spline(midmonths,seaice12([12 1:12 1]),days)))); 
tsurf_cm(:,proglacial+1)      = max(T_f,spline(midmonths,tsurf12_cml([12 1:12 1]),days));
% Initialize temperature and other array
initial_temp = linspace(4, 4, num_layers)'+T_f;
temp = initial_temp;

T3d=ones(num_layers,nt)*T_f; % for output
Tmean=ones(nt,nyrs)*NaN; % for output
dQ=zeros(nt,1);

tsurf_open=temp(1);
% Finite difference model forward in time
for yr=1:nyrs
for dd = 1:length(days)
    % Calculate sensible heat flux
    sensible_heat_flux = h * (Tair(dd) - tsurf_open); %temp(1));
    % longwave radiation upward of the lake
    lwu = emissivity_w * sigma * tsurf_open.^4;
    % Total surface heat flux over ice free regions, positive downward
    Q_surface = swd(dd) + lwd(dd) - lwu + sensible_heat_flux;
    % Update surface layer temperature using total heat flux
  
    dT = Q_surface / (rho_w * c_pw * dz)*dt;
    tsurf_open=max(T_f,(temp(1) + dT));
    temp(1) = (1-seaice(dd))*tsurf_open+seaice(dd)*T_f;
    % for proglacial=true we limit the lake surface to a maximum temperature of 4°C, 
    % consistent with the respective climate forcing 
    % dQ is the amount of energy/m**2 in Joule which must be additionally consumed
    % to achieve this cooling. 
    if proglacial
      tsurf_open=min(T_f+4,tsurf_open);  
      cool_temp=tsurf_cm(dd,2);
      dQ(dd)=(temp(1)-cool_temp)*(rho_w * c_pw * dz);
      temp(1)=cool_temp;  
    end 
    % Heat transfer in water
    % Update temperatures at  using finite difference method
    temp_new = temp;
    for i = 2:num_layers-1
        temp_new(i) = temp(i) + dt/dz*(alpha_if(i)/dz * (temp(i+1) - temp(i)) - alpha_if(i-1)/dz*(temp(i)- temp(i-1)));
    end
    temp_new(num_layers)=temp_new(num_layers-1); % no flux or gradient in bottom layer
    Tc=temp_new-T_f;
    % calculate density for all layers and enforce stable stratification 
    rho = 5.5289e-8 * Tc.^3 - 8.5016e-6 * Tc.^2 + 6.5622e-5 * Tc + 0.99987;
    [dum,idx]=sort(rho);  % shuffle(sort) watercolumn adiabatically if unstable stratification
    % Update temperature array
    temp = temp_new(idx);
    tsurf_lm(dd,proglacial+1)=temp(1);
    T3d(:,dd)=temp;
    Tmean(dd,yr)=mean(temp(1:end)-T_f);   
end
end
%For a lake of 100000km**2 = 1e11 m**2
% we can estimate the necessary amount of ice in Gt (Gt=1e12kg)
% dM = sum(dQ(:))*1e11/L_i/1e12 (Gt) of ice melting in the lake
dM = sum(dQ(:))*1e11/L_i/1e12
dQ = sum(dQ(:))
figure(1)
Tm=movmean(Tmean(:),365);
Tm=Tm(366:end-365);
plot((1:length(Tm))/365+.5,Tm,'LineWidth',2);
ylabel('T_{surf} (^o C)')

figure(2)
if proglacial
  subplot(212)
else
  subplot(211)
end
pcolor(days,-(0:9)*dz,T3d(1:10,:)-T_f)
[map,lev]=create_anom_map2(-4,8,24);
colormap(map);
caxis([0,12]);
cb=colorbar;
shading flat
ylabel(cb,'lake temperature (°C)')
ylabel('Depth (m)')
end
figure(2)
if strcmp(exper,'NAIS')
    exper=['LIS']
end

  subplot(211)
title([exper '-PL Lake Temperature (free surface)'])

  subplot(212)
title([exper '-PL Lake Temperature (ice cooled)'])
print(['../FIGS/S8_' exper '_stratif.png'],'-dpng')
tsurf12_lm=zeros(12,2);
tsurf12_cm=zeros(12,2);


for j=1:2
for k=1:12
tsurf12_lm(k,j)=mean(tsurf_lm(mths1(k):mthse(k),j));
tsurf12_cm(k,j)=mean(tsurf_cm(mths1(k):mthse(k),j));
end
end
figure(4)

plot(tsurf_lm(:,1)-T_f,'r-','LineWidth',2);
plot(tsurf_cm(:,1)-T_f,'k-','LineWidth',2);
plot(tsurf_lm(:,2)-T_f,'r--','LineWidth',2);
plot(tsurf_cm(:,2)-T_f,'k--','LineWidth',2);
plot(midmonths(2:end-1),squeeze(tsurf12_cm(:,2))-T_f,'k+');
plot(midmonths(2:end-1),tsurf12_lm(:,2)-T_f,'r+');
plot(midmonths(2:end-1),squeeze(tsurf12_cm(:,1))-T_f,'kx');
plot(midmonths(2:end-1),tsurf12_lm(:,1)-T_f,'rx');
title([exper '-PL Annual Surface Temperature '])
ylabel('lake surface temperature (°C)')
grid
legend([Cexps{1}, ' AGCM'],[Cexps{1} ' Lake Model'],[Cexps{2}, ' AGCM'],[Cexps{2} ' Lake Model'],'Location','NorthWest')
print(['../FIGS/S7' exper '_Tsurf.png'],'-dpng')
