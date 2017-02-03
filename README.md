##This is a script targeting giving a monitor of CMS pixel Phas I detector voltages, including portcard, modules, difference between them. I wrote this first part of script that we can collect information from everywehere-- Hannsjorg's spreadsheet of voltage recording, cable_map spreadsheet etc. Will asked me eight questions and I can now answer first one.

###1) What is the voltage drop (Va, Vd) between the port card and the module?
about 0.35V, and flat across different ROC ID(ROC ID is assigned according to table backer.csv).

2) What is the voltage drop between the DCDC converter and the Port Card?
(In principle we know which DCDC converter went in which spot, but you can
also measure, or get Hannsjoerg to measure, the output DCDC converter voltage
for each DCDC converter)

3) Are the values measured in 1 and 2 consistent with our expectations?
-For example: Is a low module voltage reading the result of a low port card voltage?
-Is a low port card voltage the result of a broken wire between the DC DC converter
and the port card, or is the DCDC converter having a problem?

4) I also don't think the temperature measurement using the DCU has been sorted
out yet. It would be good to follow up on this with Hannsjoerg.

5) I'm interested in this long term. I see us taking a read back calibration and measuring
the DCU (and perhaps even getting a snapshot of the CAEN values) on a regular basis
so we can see how the detector ages with time so we can keep it calibrated etc. During
LS2 (where I imagine we will take the detector out) we will have another opportunity to
measure values.

6) building a little on 6, we have been ignoring the CAEN eradicable voltages and currents,
but we should have those values in the same spot as DCU and read back values so we can
compare.

7) This will get more interesting as we get damage on the detector. The inner ROCS will see
damage firs, and their read back conversions should change the fastest. The outer ROCs should
change the least. I can imagine that at some point, we will use the outer ROC read back, and
the fact that a module must be at the same voltage for all ROCs (barring problems with some
ROCs), in order to track what happens with the detector.

8) It will also get interesting to see what happens during collisions. Knowing the CAEN voltages
and currents and the port card voltages may be our best chance at knowing what the real power
consumption is on the detector.
