import os
import xarray as xr


source_path = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1'

def list_files(path):
    for root,dirs,files in os.walk(path):
        level = root.replace(path,'').count(os.sep)
        indent = ' ' * 4 *(level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '  '*4*(level+1)
        for f in files:
            print(f'{subindent}{f}')

list_files(source_path)

def files_and_subdirectories(root_path):
    files = []
    directories = []
    for f in os.listdir(root_path):
        if os.path.isfile(f):
            files.append(f)
        elif os.path.isdir(f):
            directories.append(f)
    return directories, files

directories,files = files_and_subdirectories(source_path)

print(directories)
print(files)

file = '/mnt/d/1_protect/0_sanity_check/IMAU/IMAUICE1/abmb_32/acabf_AIS_IMAU_IMAUICE1_abmb.nc'


ds = xr.tutorial.load_dataset(file)

