# Ice Sheet Simulation compliance checker

The script checks the compliance of a simulation dataset according criteria, which are related to:

* naming conventions 
* admissible numerical values,
* spatial definition of the grid which differs according to the ice sheet (AIS vs GIS),
* time recording dependent of the experiments.

The compliance criteria of output variables are defined in a separate csv file. The compliance criteria of experiments are directly defined as a dictionnary in the python file.

=> For ISMIP6 simulations, the criteria are following the conventions defined in the [ISMIP6 wiki](https://www.climate-cryosphere.org/wiki/index.php?title=ISMIP6-Projections-Antarctica#Appendix_1_.E2.80.93_Output_grid_definition_and_interpolation). The associated csv file is [ismip6_criteria_v0.csv](https://github.com/jbbarre/ISM_SimulationChecker/blob/main/ismip6_criteria_v0.csv)

=> ISMIP6 2300 file name convention: check carrefully the section **A2.1 File name convention** of the [ISMIP6 2300 wiki](https://www.climate-cryosphere.org/wiki/index.php?title=ISMIP6-Projections2300-Antarctica)

*************************************************

### Python and dependencies

The code has been developed with python 3.9 and the following modules:

* os
* xarray
* cftime
* numpy
* pandas
* datetime
* tqdm
  
=> Conda users can install the **isscheck** environnment with the YML file [isschecker_env.yml](https://github.com/jbbarre/ISM_SimulationChecker/blob/main/isschecker_env.yml).

*************************************************

### How to launch a compliance check ?

1. In *compliance_checker_v0.py*, specify the path of the directory to check by changing the value of the variable **source_path**. The compliance criteria csv file must be located in the directory as the py file.

2. In a terminal, run the script:
`> python compliance_checker_v0.py`.

3. The script creates a *compliance_checker_log.txt* file in the source_path, which reports the errors and warnings.


*************************************************

### Test the code

1. Conda users: activate the isschecker environnement: `> conda activate isschecker`. For others, be sure that the dependencies specified in the YML file [isschecker_env.yml](https://github.com/jbbarre/ISM_SimulationChecker/blob/main/isschecker_env.yml) are installed. 
   
2. in a terminal, run the script: `> python compliance_checker_v0.py`. A progression bar appears in the terminal and shows the progression.
   
3. Without any changes, the script checks the `test` directory, which contains a single file. After processing the check, open the *compliance_checker_log.txt* file created in the `test` directory. The compliance checker raises errors because the test data is just a short extraction of a complete dataset.
   
