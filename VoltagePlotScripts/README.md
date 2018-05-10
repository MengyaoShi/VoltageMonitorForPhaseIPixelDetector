------------------
Vd and Va plots by ROC or BLD 
------------------

To see values as a function of ROC (and combined averages ordered by radius), run mod_readback_simple_ROC.py:

       python mod_readback_simple_ROC.py

The script will loop through the list of months in the code, reading Readbacker_[month].dat. New months must be added to the list. Outputs are plots_[month].root.

To see voltages as a function of BLD, run mod_readback_simple_BLD.py with the .dat file as arguement:

       python mod_readback_simple_BLD.py Readbacker.dat

__________________
Comprehensive Voltages Plots (very old, depends on voltages recorded by hand when HC is outside detector)
------------------

Execute mod_readback.py to create new everything.csv with DCDC voltages added to sheet. The script also creates it's own abridged list of values and uses it to create plots of the three main measurements. 

The script requires the csv file titles as input. 

Example:

	python mod_readback.py Readbacker_BpO.dat DCDC_BpO.csv map_BpO.csv DCU_BpO.csv

Readbacker_BpO.dat is the POS output with module voltages. DCDC_BpO.csv is the google doc sheet with the direct DCDC measurements. map_BpO.csv is the sheet with the mapping between modules and portcards/ports. DCU_BpO.csv is Mengyao's everything.csv sheet.
