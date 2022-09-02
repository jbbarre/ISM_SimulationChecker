
import os
import xarray as xr
import pandas as pd
import datetime
import numpy as np
#decoding time units and variable values in a netCDF file conforming to the Climate and Forecasting (CF) netCDF conventions.
import cftime
# progress bar
from tqdm import tqdm

###  Version :
version = '0.1' #05.08.2022 (Major version).(Minor version)

#######################################
#### specify your source path
#######################################
source_path = './test'

#######################################
# Compliance values to be monitored
#######################################
workdir = os.getcwd()

try:
    # load csv :
    ismip  = pd.read_csv(workdir + '/ismip6_criteria.csv',delimiter=';',decimal=",")
except IOError:
    print('ERROR: Unable to open the compliance criteria file (.csv required with ; as delimiter and , for decimal.). Is the path to the file correct ? '+ workdir + 'ismip6_criteria_v0.csv')
else:
    ismip_meta = ismip.to_dict('records')
    # get the list of variables
    ismip_var = [dic['variable'] for dic in ismip_meta]
    # get the mandatory variables
    ismip_mandatory_var = ismip['variable'][ismip.mandatory==1].tolist()

    variables = ismip_var
    mandatory_variables = ismip_mandatory_var
    
# experiments ISMIP6 extension (2300) setup 
experiments_ismip6_ext =[{'experiment':'ctrlAE', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,7,1),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE01', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE02', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE03', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE04', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE05', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE06', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE07', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE08', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE09', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE10', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE11', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE12', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE13', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286},
                  {'experiment':'expAE14', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2300,6,30),'endsup':datetime.datetime(2301, 1, 1),'duration':286}
]  

# experiments ISMIP6 setup 
experiments_ismip6 =[{'experiment':'hist', 'startinf':datetime.datetime(1979, 6, 30),'startsup':datetime.datetime(1980, 1, 1),'endinf':datetime.datetime(2014, 6, 30),'endsup':datetime.datetime(2015, 1, 1),'duration':35},
                  {'experiment':'ctrl', 'startinf':datetime.datetime(1979, 6, 30),'startsup':datetime.datetime(1980, 1, 1),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':120},
                  {'experiment':'ctrl_proj', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,7,1),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp01', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp02', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp03', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp04', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp05', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp06', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp07', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp08', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp09', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp10', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp11', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp12', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86},
                  {'experiment':'exp13', 'startinf':datetime.datetime(2015, 1, 1),'startsup':datetime.datetime(2016, 1, 2),'endinf':datetime.datetime(2100,6,30),'endsup':datetime.datetime(2101, 1, 1),'duration':86}
]

scalar_variables_ismip6 = ['lim','limnsw','iareagr','iareafl','tendacabf','tendlibmassbf','tendlibmassbffl','tendlicalvf','tendlifmassbf','tendligroundf']
scalar_variables = scalar_variables_ismip6
experiments = experiments_ismip6_ext

# obtain the directory tree : return directories (=experiments) and files (=variables)
def files_and_subdirectories(path):
    files = []
    directories = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
             files.append(f)
        elif os.path.isdir(os.path.join(path, f)):
            directories.append(f)
    return directories, files

# check motonocity of a list (used to check time serie) 

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

###############################################
# create the compliance_checker_log.txt file
###############################################

# stop the checker if Typeerror occurs.
try:

    with open(os.path.join(source_path,'compliance_checker_log.txt'),"w") as f:
        print('-> Checking '+ source_path)
        print( )
        experiment_directories,files = files_and_subdirectories(source_path)
        today = datetime.date.today()

        f.write('************************************************************************************\n')
        f.write('*************     Ice Sheet Model Simulations - Compliance Checker     *************\n')
        f.write('************************************************************************************\n')
        f.write(f'version: {version} \n')
        f.write('verification criteria: ismip6_criteria_v0.csv \n')
        f.write('date: '+ today.strftime("%Y/%m/%d") +'\n')
        f.write('source: https://github.com/jbbarre/ISM_SimulationChecker \n')
        f.write(' \n')
        f.write('------------------------------------------------------------------------------------\n')
        f.write('Verified directory: '+ source_path +' \n')
        f.write('------------------------------------------------------------------------------------\n')
        f.write(' \n')
        f.write(' \n')
        f.write(' \n')
        f.write(' \n')
        f.write('====================================================================================\n')
        f.write('================                DETAILED RESULTS                    ================\n')
        f.write('====================================================================================\n')
        f.write('Tips: Use Cltr+F to look for specific problems. \n')
        f.write(' \n')

        ###############################################
        # Start the compliance checker
        ###############################################

        # total number of errors for the entire compliance check. 
        total_errors = 0
        # total number of warnings for the entire compliance check. 
        total_warnings = 0
        # total number of errors related to naming tests for the entire compliance check.
        total_naming_errors = 0
        # total number of errors related to numerical tests for the entire compliance check.
        total_num_errors = 0
        # total number of errors related to spatial tests for the entire compliance check.
        total_spatial_errors = 0
        # total number of errors related to time tests for the entire compliance check.
        total_time_errors = 0
        # total number of errors related to missing mandatory files (= mandatory variables).
        total_file_errors = 0 

        # gather all the naming issues to report in the synthesis.
        report_naming_issues =[]

        #initialize  files checked counter
        file_counter = 0
        #initialize  files checked counter
        exp_counter = 0
        for xp in experiment_directories:

            exp_counter += 1

            exp_dir,exp_files = files_and_subdirectories(os.path.join(source_path, xp))
            exp_files=list(filter(lambda file: file.split('.')[-1] == 'nc', exp_files))
            
            # total number of errors for the experiment.
            exp_errors = 0
            # total number of errors related to naming tests of the experiment.
            exp_naming_errors = 0
            # total number of errors related to numerical tests of the experiment.
            exp_num_errors = 0
            # total number of errors related to spatial tests of the experiment.
            exp_spatial_errors = 0
            # total number of errors related to time tests of the experiment.
            exp_time_errors = 0
            # total number of errors related to files(=variables) in the experiment.
            exp_file_errors = 0
            # total number of warnings for the experiment.
            exp_warnings = 0
            # total number of warnings related to naming tests of the experiment.
            exp_naming_warnings = 0
            # total number of warnings related to numerical tests of the experiment.
            exp_num_warnings = 0
            # total number of warnings related to spatial tests of the experiment.
            exp_spatial_warnings = 0
            # total number of warnings related to time tests of the experiment.
            exp_time_warnings = 0

            # create the list of missing mandatory variables - List could be empty - 
            for i in exp_files:
                file_name_split = i.split('_')
                variable = file_name_split[0]
                temp_mandatory_var = mandatory_variables
                if  variable in mandatory_variables:
                    temp_mandatory_var.remove(variable)
            #split the experiment directory name
            experiment_chain = xp.split('_')
            #get the experiment name (example: exp05)
            experiment_name = '_'.join(experiment_chain[:-1])
            #get the resolution as integer
            grid_resolution = int(experiment_chain[-1])
            
            if experiment_name  in [dic['experiment'] for dic in experiments]:
                f.write('\n ')
                f.write('**********************************************************\n')
                f.write(' ** Experiment: ' + experiment_name + ' \n ')
                f.write('**********************************************************\n')
                f.write('\n ')
                if not temp_mandatory_var:
                    f.write('Mandatory variables Test: ' + xp + ' : all mandatory variables exist. \n')
                else:
                    f.write('ERROR: In experiment ' +  xp +', these mandatory variable(s) is (are) missing: '+ str(temp_mandatory_var)+'\n')
                    exp_file_errors += len(temp_mandatory_var)

                for file in tqdm(exp_files):

                    file_counter += 1

                    # total number of errors for the variable.
                    var_errors = 0
                    # total number of warnings for the variable.
                    var_warnings = 0
                    # total number of errors related to the naming tests of the variable.
                    var_naming_errors = 0
                    # total number of errors related to the numerical tests of the variable.
                    var_num_errors = 0
                    # total number of errors related to the spatial tests of the variable.
                    var_spatial_errors = 0
                    # total number of errors related to the time tests of the variable.
                    var_time_errors = 0


                    # total number of warnings for the variable.
                    var_warnings = 0
                    # total number of warnings for the variable.
                    var_warnings = 0
                    # total number of warnings related to the naming tests of the variable.
                    var_naming_warnings = 0
                    # total number of warnings related to the numerical tests of the variable.
                    var_num_warnings = 0
                    # total number of warnings related to the spatial tests of the variable.
                    var_spatial_warnings = 0
                    # total number of warnings related to the time tests of the variable.
                    var_time_warnings = 0

                    split_path=os.path.normpath(file).split(os.sep)
                    file_name = split_path[-1]
                    file_name_split = file_name.split('_')
                    
                    considered_variable = file_name_split[0]
                    region = file_name_split[1]
                    group  = file_name_split[2]
                    model = file_name_split[3]
                    file_extention = file_name_split[len(file_name_split)-1][-2:]
                    
                    # Load the netcdf file
                    ds = xr.open_dataset(os.path.join(source_path,xp,file))

                    # Load local variables included in the netcdf file
                    file_variables = list(ds.data_vars)

                    # test file extention

                    if file_extention != 'nc':
                        f.write(' !! ' + file_name + ' is not a NETCDF file. The compliance check is ignored.'+'\n')
                        #f.write (' \n')
                        
                    else: 
                        # test if the structure of the file name is correct
                        if int(len(file_name_split)) == 5:
                            # NAMING TEST
                            # test if experiment name (host directory) and exp in variable file name are the same.
                                            # name of the experiment in the file name.
                            experiment_varname = file_name_split[4][:-3]
                            if experiment_varname == experiment_name:
                                # test IF the file is not a scalar variable then run check ELSE check next variable
                                if considered_variable in variables:
                                    f.write (' \n')
                                    f.write('Experiment: '+ experiment_name + ' - File: ' + file_name + '\n')
                                    f.write(' \n')

                                    # TEST data dimensions: x,y,t ok?
                                    header_ds = ds.to_dict(data=False)
                                    dim = set(list(header_ds['coords'].keys()))

                                    #perform compliance even is time is missing. check on time is managed below
                                    if set(['x','y']).issubset(dim):
                                        # NAMING TEST
                                        if region.upper() in ['AIS', 'GIS']:
                                            #f.write('Studied Region: ' + region + '\n')
                                            if region == 'AIS':
                                                # AIS Grid
                                                grid_extent = [-3040000,-3040000,3040000,3040000]
                                                possible_resolution = [1,2,4,8,16,32] 
                                            else: 
                                                # GIS Grid
                                                grid_extent = [-720000,-3450000,960000,-570000]
                                                possible_resolution = [1,2,4,5,10,20]


                                            for ivar in file_variables:
                                                if ivar in ismip_var:
                                                    f.write('** Tested Variable: '+ ivar +'\n')
                                                    f.write (' \n')
                                                    # get index in the ismip_var list
                                                    var_index = [k for k in range(len(ismip_var)) if ismip_var[k]==ivar]
                                                    
                                                # NUMERICAL TESTS
                                                    f.write('NUMERICAL Tests \n')
                                                    # check the unit
                                                    if ds[ivar].attrs['units'] == ismip_meta[var_index[0]]['units']:
                                                        f.write(' - The unit is correct: ' + ds[ivar].attrs['units']+'\n')
                                                    else:
                                                        f.write(' - ERROR: The unit of the variable is ' + ds[ivar].attrs['units'] + ' and should be ' + ismip_meta[var_index[0]]['units']+' \n')
                                                        var_num_errors += 1 

                                                    # check if the array  is full of NAN values
                                                    if False in ds[ivar].isnull():
                                                        # check the min value
                                                        if ds[ivar].min(skipna=True).item()>=ismip_meta[var_index[0]]['min_value_'+region.lower()]:
                                                           f.write(' - The minimum value successfully verified.\n')
                                                        else:
                                                            f.write(' - ERROR: The minimum value (' + str(ds[ivar].min(skipna=True).values.item(0)) + ') is out of range. Min value accepted: ' + str(ismip_meta[var_index[0]]['min_value_'+region.lower()])+'\n')
                                                            var_num_errors += 1 
                                                        # check the max value
                                                        if ds[ivar].max(skipna=True).item()<=ismip_meta[var_index[0]]['max_value_'+region.lower()]:
                                                                f.write(' - The maximum value successfully verified.\n')
                                                        else:
                                                            f.write(' - ERROR: The maximum value (' + str(ds[ivar].max(skipna=True).values.item(0)) + ') is out of range. Max value accepted: ' + str(ismip_meta[var_index[0]]['max_value_'+region.lower()])+'\n')
                                                            var_num_errors += 1
                                                    else:
                                                        f.write(' - ERROR: The array only contains Nan values.\n')
                                                        var_num_errors += 1


                                                # SPATIAL TESTS
                                                    # SPATIAL:Check spatial extent of the grid
                                                    f.write('SPATIAL Tests \n')
                                                    # get the grid from the file
                                                    coords = ds.coords.to_dataset()
                                                    Xbottomleft=int(min(coords['x']).values.item())
                                                    Ybottomleft=int(min(coords['y']).values.item())
                                                    Xtopright=int(max(coords['x']).values.item())
                                                    Ytopright=int(max(coords['y']).values.item())

                                                    if Xbottomleft == grid_extent[0] & Ybottomleft == grid_extent[1]:
                                                        f.write(' - Grid: Lowest left corner is well defined.\n')
                                                    else:    
                                                        f.write(' - ERROR: Lowest left corner of the grid [' + str(Xbottomleft) + ',' + str(Ybottomleft) + '] is not correctly defined. [' + str(grid_extent[0])+ ',' + str(grid_extent[1]) + '] Expected\n')
                                                        var_spatial_errors += 1
                                                    if Xtopright == grid_extent[2] & Ytopright == grid_extent[3]:
                                                        f.write(' - Grid: Upper right corner is well defined.\n')
                                                    else:    
                                                        f.write(' - ERROR: Upper rigth corner of the grid [' + str(Xtopright) + ',' + str(Ytopright) + '] is not correctly defined. [' + str(grid_extent[0]) + ',' + str(grid_extent[1])+ '] Expected\n')
                                                        var_spatial_errors += 1

                                                    #SPATIAL:check the spatial resolution
                                                    Xresolution = round((coords['x'][1].values-coords['x'][0].values)/1000,0)
                                                    Yresolution = round((coords['y'][1].values-coords['y'][0].values)/1000,0)
                                                    if Xresolution in set(possible_resolution) and Yresolution in set(possible_resolution):
                                                        if Xresolution == grid_resolution and Yresolution == grid_resolution:
                                                            f.write(' - The grid resolution (' + str(Xresolution) + ') was successfully verified.\n')
                                                        else:
                                                            f.write(' - ERROR: The grid resolution ( ' + str(Xresolution) + ' or ' + str(Yresolution) + ') is different of ' + str(grid_resolution) + 'declared in the file name.\n')
                                                            var_spatial_errors += 1
                                                    else:
                                                        f.write(' - Error: x: ' + str(Xresolution) + ',y: ' + str(Yresolution) + ' is not an authorized grid resolution.\n')
                                                        var_spatial_errors += 1

                                                # TIME TESTS
                                                    f.write('TIME Tests \n')
                                                    #check if time dimension is not missing
                                                    if set(['t']).issubset(dim) or set(['time']).issubset(dim):
                                                        iteration = len(ds.coords['time'])
                                                        start_exp = pd.to_datetime(min(ds['time']).values.astype("datetime64[ns]"))
                                                        end_exp  = pd.to_datetime(max(ds['time']).values.astype("datetime64[ns]"))
                                                        avgyear = 365.2425        # pedants definition of a year length with leap years
                                                        
                                                        index_exp=[dic['experiment'] for dic in experiments].index(experiment_name)
                                                        #test if start_exp and end_exp are datetime format
                                                        if isinstance(start_exp, datetime.datetime) & isinstance(end_exp, datetime.datetime):
                                                            #check Monotonicity of the time serie
                                                            if strictly_increasing(ds.coords['time']):
                                                                # test Time step : should be 360<timestep<367
                                                                if isinstance((ds['time'].values[1]-ds['time'].values[0]),datetime.timedelta):
                                                                    time_step = (ds['time'].values[1]-ds['time'].values[0]).days
                                                                else:   
                                                                    if isinstance((ds['time'].values[1]-ds['time'].values[0]),np.timedelta64):
                                                                        time_step = np.timedelta64(ds['time'].values[1]-ds['time'].values[0], 'D')/ np.timedelta64(1, 'D')
                                                                    else:    
                                                                        time_step = ds['time'].values[1]-ds['time'].values[10]

                                                                if 360<=time_step<=367:
                                                                    f.write(' - Time step: ' + str(time_step) + ' days' + '\n')
                                                                else:
                                                                    f.write(' - ERROR: the time step(' + str(time_step) + ') should be comprised between [360,367].\n')
                                                                    var_time_errors += 1

                                                                # test duration  (iteration = length of the coords 'time')
                                                                duration_days = pd.to_timedelta(time_step * iteration,'D')
                                                                duration_years = round(pd.to_numeric(duration_days.days / avgyear))
                                                                if  duration_years == experiments[index_exp]['duration']:
                                                                    f.write(" - Experiment lasts " + str(duration_years) + ' years.\n')
                                                                    # test Starting date
                                                                    if experiments[index_exp]['startinf'] <= start_exp <= experiments[index_exp]['startsup']:
                                                                        f.write(' - Experiment starts correctly on ' + start_exp.strftime('%Y-%m-%d') + '.\n')
                                                                    else:
                                                                        f.write(' - ERROR: the experiment starts the ' + start_exp.strftime('%Y-%m-%d') + '. The date should be comprised between ' + experiments[index_exp]['startinf'].strftime('%Y-%m-%d') + ' and ' + experiments[index_exp]['startsup'].strftime('%Y-%m-%d')+'\n')
                                                                        var_time_errors += 1
                                                                    # test Ending date
                                                                    if experiments[index_exp]['endinf'] <= end_exp <= experiments[index_exp]['endsup']:
                                                                        f.write(' - Experiment ends correctly on ' + end_exp.strftime('%Y-%m-%d') + '.\n')
                                                                    else:
                                                                        f.write(' - ERROR: the experiment ends on ' + end_exp.strftime('%Y-%m-%d') + '. The date should be comprised between ' + experiments[index_exp]['endinf'].strftime('%Y-%m-%d') + ' and ' + experiments[index_exp]['endsup'].strftime('%Y-%m-%d')+'\n')
                                                                        var_time_errors += 1
                                                                else:
                                                                    end_date = start_exp  + datetime.timedelta(days = experiments[index_exp]['duration']*avgyear)
                                                                    f.write(' - ERROR: the experiment lasts ' + str(duration_years) + ' years. The duration should be ' + str(experiments[index_exp]['duration']) + ' years\n')
                                                                    f.write(' - As the experiment started on ' + start_exp.strftime('%Y-%m-%d') + ' , it should end on '+ end_date.strftime('%Y-%m-%d')+'\n')                                                                 
                                                                    var_time_errors += 1


                                                            else: #time serie not monotonous
                                                                f.write(' - ERROR: the time serie is not monotonous. Time segments have probably been concatenate in a wrong order.\n')
                                                                var_time_errors += 1
                                                            
                                                        else: 
                                                            #not a datetime format
                                                            f.write(' - ERROR: the time format of the Netcdf file is not recognized.Time Tests have been ignored.\n')
                                                            var_time_errors += 1
                                                    else: #Time dimension is missing
                                                        f.write(' - ERROR: The time dimensions is missing. Time Tests have been ignored.\n')
                                                        var_time_errors += 1

                                        else:
                                            # NAMING TEST
                                            f.write('- ERROR: Region ' + region + ' not recognized. It should be AIS or GIS. The compliance check has been interrupted for this variable.\n')
                                            report_naming_issues.append('Compliance check ignored: region (AIS/GIS) not identified in the file ' + file_name + ' due to wrong naming.')
                                            var_naming_errors += 1
                                    else:
                                        ## TEST data dimensions: x or y is missing
                                        f.write('- ERROR: Compliance check ignored: x or y in the mandatory dimensions (x,y,t) is missing.\n')
                                        f.write('                                   Only ' + str(list(header_ds['coords'].keys())) + ' has been detected.\n')
                                        report_naming_issues.append('Compliance check ignored: x or y in the mandatory dimensions (x,y,t) is missing in ' + file_name )
                                        var_naming_errors += 1

                                    var_errors = var_errors + var_naming_errors + var_num_errors + var_spatial_errors + var_time_errors
                                    var_warnings = var_warnings + var_num_warnings + var_spatial_warnings + var_time_warnings
                                    
                                    f.write('\n')        
                                    f.write('----------------------------------------------------------\n')
                                    f.write(experiment_name + ' - ' + considered_variable + ' - File:' + file_name+'\n')
                                    if var_errors > 0:
                                        f.write(str(var_errors) + ' error(s). Please review before sharing.'+'\n')
                                    else:
                                        f.write('No errors. Good job !'+'\n')
                                    if var_warnings > 0:
                                        f.write(str(var_warnings) + ' warning(s). Please review before sharing.'+'\n')
                                    else:
                                        f.write('No warnings.'+'\n')
                                    f.write('----------------------------------------------------------\n')
                            else:
                                # NAMING TEST
                                f.write(' - ERROR: in the file name ' + file_name + ', the experiment name ('+experiment_varname+') do not match the directory name: ' + experiment_name + '.\n')
                                report_naming_issues.append('Compliance check ignored: in the file name ' + file_name + ', the experiment name (' + experiment_varname + ') do not match the directory name: ' + experiment_name + '.\n')
                                var_naming_errors += 1

                                var_errors = var_errors + var_naming_errors + var_num_errors + var_spatial_errors + var_time_errors
                                var_warnings = var_warnings + var_num_warnings + var_spatial_warnings + var_time_warnings

                        else: 
                            # NAMING TEST
                            f.write(' - ERROR: the file name ' + file_name + ' do not follow the naming convention.\n')
                            report_naming_issues.append('Compliance check ignored: file ' + file_name + ' do not follow the naming convention.')
                            var_naming_errors += 1

                            var_errors = var_errors + var_naming_errors + var_num_errors + var_spatial_errors + var_time_errors
                            var_warnings = var_warnings + var_num_warnings + var_spatial_warnings + var_time_warnings

                    exp_naming_errors = exp_naming_errors + var_naming_errors
                    exp_num_errors = exp_num_errors + var_num_errors
                    exp_spatial_errors = exp_spatial_errors + var_spatial_errors
                    exp_time_errors = exp_time_errors + var_time_errors   
                    exp_errors = exp_time_errors + exp_spatial_errors + exp_num_errors + exp_naming_errors+exp_file_errors
                    exp_num_warnings = exp_num_warnings + var_num_warnings
                    exp_spatial_warnings = exp_spatial_warnings + var_spatial_warnings
                    exp_time_warnings = exp_time_warnings + var_time_warnings
                    

            else:
                f.write('\n ')
                f.write('**********************************************************\n')
                f.write(' **  Experiment: ' + experiment_name + ' \n ')
                f.write('**********************************************************\n')
                f.write('\n ')
                f.write('ERROR: The compliance check is ignored for experiment ' + experiment_name + ' as it is not in [hist, ctrl, ctrl_proj, exp01, exp02, exp03, exp04, exp05, exp06, exp07, exp08, exp09, exp10, exp11, exp12, exp13]. \n')
                exp_naming_errors +=1
                exp_errors = exp_time_errors + exp_spatial_errors + exp_num_errors + exp_naming_errors + exp_file_errors
                report_naming_issues.append('Compliance check ignored : experiment ' + experiment_name + ' not in the experiments list.')
        
            print(experiment_name,': compliance check processed.')
            if exp_errors >0:
                print('Found' , exp_errors , 'errors. Check compliance_checker_log.txt for details.')
            else:
                print('Successfully verified with no errors')
            print( )

            # Update counters.
            total_naming_errors += exp_naming_errors
            total_num_errors += exp_num_errors
            total_spatial_errors += exp_spatial_errors
            total_time_errors += exp_time_errors
            total_file_errors += exp_file_errors
            

        total_errors = total_naming_errors + total_num_errors + total_spatial_errors + total_time_errors + total_file_errors
        #feedback terminal
        print('-------------------------------------------------------------------------')
        print(source_path,': compliance check processed.')
        if total_errors >0:
            print('Found a total of' , total_errors , 'errors. Check compliance_checker_log.txt for details.')
        else:
            print('Successfully verified with no errors')
        print('-------------------------------------------------------------------------')
            

    ###################################################        
    # insert synthesis at the top of the log file
    ###################################################

    with open(os.path.join(source_path,'compliance_checker_log.txt'), "r") as f:
        contents = f.readlines()
    # lines insert position
    iline =  11
    contents.insert(iline, str(exp_counter) + ' experiments checked.\n')
    iline += 1
    contents.insert(iline, str(file_counter) + ' files checked (Scalar files are ignored).\n')
    iline += 2
    contents.insert(iline, str(total_errors) + ' error(s) detected.\n')
    iline += 1
    contents.insert(iline, '  - Mandatory variables: ' + str(total_file_errors) + ' error(s)\n')
    iline += 1 
    contents.insert(iline, '  - Naming Tests       : ' + str(total_naming_errors) + ' error(s)\n')
    iline += 1
    contents.insert(iline, '  - Numerical Tests    : ' + str(total_num_errors) + ' error(s)\n')
    iline += 1 
    contents.insert(iline, '  - Spatial Tests      : ' + str(total_spatial_errors) + ' error(s)\n')
    iline += 1
    contents.insert(iline, '  - Time Tests         : ' + str(total_time_errors) + ' error(s)\n')
    iline += 2
    contents.insert(iline, str(total_warnings) + ' warning(s) detected.\n')
    iline += 2
    if total_naming_errors > 0 :
        contents.insert(iline, 'Naming tests errors report: \n' )
        iline += 1
        for i in range(iline,len(report_naming_issues)):
            contents.insert(i, '  - ' + report_naming_issues[i-24] + '\n')
        contents.insert(iline+len(report_naming_issues), '\n')

    with open(os.path.join(source_path,'compliance_checker_log.txt'), "w") as f:
        f.writelines(contents)

except TypeError:
    print('Something went wrong with your dataset. Please, check your file(s) carrefully.') 

