------------------
Vd and Va plots by ROC or BLD 
------------------

To see voltages as a function of ROC (and combined ROC ordered by radius), run mod_readback_simple_ROC.py with the .dat file as arguement:

       python mod_readback_simple_ROC.py Readbacker.dat

To see voltages as a function of BLD, run mod_readback_simple_BLD.py with the .dat file as arguement:

       python mod_readback_simple_BLD.py Readbacker.dat

Output is plots.root unless changed in the script. 
__________________
Comprehensive Voltages Plots
------------------

Execute mod_readback.py to create new everything.csv with DCDC voltages added to sheet. The script also creates it's own abridged list of values and uses it to create plots of the three main measurements. 

The script requires the csv file titles as input. 

Example:

	python mod_readback.py Readbacker_BpO.dat DCDC_BpO.csv map_BpO.csv DCU_BpO.csv

Readbacker_BpO.dat is the POS output with module voltages. DCDC_BpO.csv is the google doc sheet with the direct DCDC measurements. map_BpO.csv is the sheet with the mapping between modules and portcards/ports. DCU_BpO.csv is Mengyao's everything.csv sheet.
