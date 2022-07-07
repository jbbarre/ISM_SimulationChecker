
import os
import xarray as xr
import pandas as pd
import datetime
import numpy as np


ismip  = pd.read_csv('/mnt/d/1_protect/0_sanity_check/ismip_variable.csv',delimiter=';')
ismip_meta = ismip.to_dict('records')
ismip_var = [dic['variable'] for dic in ismip_meta]


#file = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1/exp05_32/acabf_AIS_IMAU_IMAUICE1_exp05.nc'
#!scalar! file = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1/abmb_32/iareafl_AIS_IMAU_IMAUICE1_abmb.nc'
#file = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1/exp05_32/libmassbffl_AIS_IMAU_IMAUICE1_exp05.nc'
file = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1/exp05_32/orog_AIS_IMAU_IMAUICE1_exp05.nc'
ds = xr.open_dataset(file)

file_var = list(ds.data_vars)
errors = 0
warnings = 0

for ivar in file_var:
    if ivar in ismip_var:
        print('* ',ivar, 'is a valid name.')
        # get index in the ismip_var list
        var_index = [k for k in range(len(ismip_var)) if ismip_var[k]==ivar]
        # TEST1 - check the unit
        if ds[ivar].attrs['units'] == ismip_meta[var_index[0]]['units']:
            print('the unit is correct:',ds[ivar].attrs['units'])

        else:
            print('the current variable\'s unit is',ds[ivar].attrs['units'],'and should be',ismip_meta[var_index[0]]['units'],'Please check.')
            warnings = warnings + 1 
        # TEST2 - check the min,max,mean values
        if ds[ivar].min()>ismip_meta[var_index[0]]['min_value']:
            print('The minimum value successfully verified.')
        else:
            print('The minimum value(', round(ds[ivar].min().values.item(0),5),') is out of range. Please check it!')
            errors = errors + 1 
        if ds[ivar].max()>ismip_meta[var_index[0]]['max_value']:
                print('The maximum value successfully verified.')
        else:
            print('The maximum value(', round(ds[ivar].max().values.item(0),5),') is out of range. Please check it!')
            errors = errors + 1

        #SPATIAL: Check spatial extent of the grid
        coords = ds.coords.to_dataset()
        Xbottomleft=int(min(coords['x']).values.item())
        Ybottomleft=int(min(coords['y']).values.item())
        Xtopright=int(max(coords['x']).values.item())
        Ytopright=int(max(coords['y']).values.item())

        if Xbottomleft == -3040000 & Ybottomleft == -3040000:
            print( 'Lowest left corner of the grid is well defined.')
        else:    
            print('Lowest left corner of the grid is not well defined. [-3040000,-3040000] Expected')
            errors = errors + 1
        if Xtopright ==3040000 & Ytopright ==3040000:
            print('Upper right corner is well defined.')
        else:    
            print('Upper rigth corner of the grid is not well defined. [3040000,3040000] Expected')
            errors = errors + 1

        #SPATIAL:check the spatial resolution
        spatial_resolution = 32
        Xresolution = (coords['x'][1].values-coords['x'][0].values)/1000
        Yresolution = (coords['y'][1].values-coords['y'][0].values)/1000
        if Xresolution == spatial_resolution and Yresolution == spatial_resolution:
            print('The spatial resolution (grid size) was successfully verified.')
        else:
            print('The spatial resolution ( ', Xresolution,'or',Yresolution,') is different of ',spatial_resolution,' km. Please check it!','\n')
            error = error + 1

        # Time: experiment duration
        start_exp = min(ds['time']).values.astype('datetime64[D]')
        end_exp  = max(ds['time']).values.astype('datetime64[D]')
        print("Start of the experiment:", start_exp.astype('datetime64[D]'))
        print("End of the experiment:", end_exp.astype('datetime64[D]'))

        # Time: time resolution
        time_step = ds['time'].values[11]-ds['time'].values[10]
        print('Time step:',time_step.astype('timedelta64[D]').item().days,'days','\n')

    else:
        print(ivar,'isn\'t a known variable name. Its verification has been ignored.','\n')

print(errors,' critical errors identified in',file,'. It can\'t be shared as it is.')
print(errors,' warnings identified in',file,'. Please, check before sharing.')



