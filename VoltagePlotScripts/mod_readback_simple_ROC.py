#!/user/local/bin/python
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

gStyle.SetOptStat(0)

# NOT USED
VbgSlopeADC = TFile("GRAYvSlope.root", "read")
GRAYvSlope = VbgSlopeADC.Get("ErfFit")

# Perc Shift Vbg With DOSE
VbgPercShiftDose = TFile("PercShiftVbg_Dose.root","read")
PercVDose = VbgPercShiftDose.Get("ErfFit")

# ADC shift with radiation, from dose corrected Vbg RNG1
ShiftR1ADC = TFile("ShiftR1ADC.root","read")
scalingR1ADC = ShiftR1ADC.Get("LnFit")

# ADC shift with radiation, from dose corrected Vbg RNG2
ShiftR2ADC = TFile("ShiftR2ADC.root","read")
scalingR2ADC = ShiftR2ADC.Get("LnFit")

DividoGram = TH1F("DividoGram", "threes", 8 ,0 ,8)
for i in range (0,9):
    DividoGram.SetBinContent(i,3.)

C_R1 = 22.7
C_R2 = 22.7

#C_R1 = 22.7
#C_R2 = 34.5

#C_R1 = 16.5
#C_R2 = 28.0

#C_R1 = float(sys.argv[1])
#C_R2 = float(sys.argv[2])
 
ADCs = ['vd','va','vana','vbg']
ADCIndex = {'vd':4,'va':5,'vana':6,'vbg':7}

VALS = ['Vd','Va','Vdr','Var','Vbg','VbgCor','dose','VdCor','VaCor','VdrCor','VarCor','VbgFullCor','CorVdr','CorVar','CorVbg']
abrevVALS = ['Vd','Va','Vdr','Var','Vbg','VbgCor','dose','VdCor','VaCor']
DISKS = ['1','2','3']
MEAS = ['May','Jul','Aug','Sept','Dec']

valINDEX = {'Vd': 9, 'Va': 10, 'Vdr': 4, 'Var': 5, 'Vbg': 7, 'VbgCor': 11, 'dose': 12, 'VdCor': 13, 'VaCor': 14, 'VdrCor': 15, 'VarCor': 16, 'VbgFullCor': 17, 'CorVdr': 18, 'CorVar': 19, 'CorVbg': 20}
lumINDEX = {'May': 0.0, 'Jul': 6.3, 'Aug': 18.1, 'Sept': 24.2, 'Oct': 40.73, 'Dec': 49.98, 'Mar': 49.98}

OUTDATA = open('out.csv', 'w')

topLine = ''

def returnCombROC(roc):
    if roc < 8:
        return roc
    else:
        return (15 - roc)

def returnRadius(rng, roc):
    returnVal = 0.
    radiusUnit = 7 - int(returnCombROC(roc))
    if rng == 1:
        returnVal = 4.5 + radiusUnit*0.81
    elif rng == 2:
        returnVal = 9.6 + radiusUnit*0.81
    #print 'RNG: ' + str(rng) + ' ROC POSUNIT: ' + str(radiusUnit) + ' BIN POS: ' + str(returnCombROC(roc)) + '  radius: ' + str(returnVal)
    return returnVal

def returnDose(roc,lum,rng):
    radius = returnRadius(rng,roc)
    dose = 0.0
    if rng == 1:
        dose = .001 * C_R1 * (lum) * pow(radius,-1.5)
    if rng == 2:
        dose = .001 * C_R2 * (lum) * pow(radius,-1.5)
    return dose

def returnVbgShift(dose):
    perc = PercVDose.Eval(dose)
    returnVal = 1 + (perc*.01)
    return returnVal

def convertVbg(VbgADC,roc,lum,rng):
    radius = returnRadius(rng,roc)
    dose = 0.0
    if rng == 1:
        dose = .001 * C_R1 * (lum) * pow(radius,-1.5)
    if rng == 2:
        dose = .001 * C_R2 * (lum) * pow(radius,-1.5)
    shift = returnVbgShift(dose)
    Vbg = (1/shift) * VbgADC
    return Vbg

def correctADC(ADC,roc,lum,rng):
    radius = returnRadius(rng,roc)
    dose = 0.0
    perc = 0.0
    if rng == 1:
        dose = .001 * C_R1 * (lum) * pow(radius,-1.5)
        perc = scalingR1ADC.Eval(dose)
    if rng == 2:
        dose = .001 * C_R2 * (lum) * pow(radius,-1.5)
        perc = scalingR2ADC.Eval(dose)
    CorADC = (1/perc) * ADC
    return CorADC

for M in MEAS:
    badCount = 0
    goodCount = 0
    totalCount = 0
    tempModIdent = []
    tempModHi = []
    tempModZero = []
    tempModUsed = []
    tempModLow = []
    print "Measurment: " + str(M)
    INDATA_MOD1 = open("Readbacker_"+M+".dat")
    INDATA_MOD2 = open("Readbacker_"+M+".dat")
    p = TFile("plots_"+M+".root", "recreate")
    #CREATE ROC LIST
    RB_ROC_LIST = []
    for line1 in INDATA_MOD1:
       FULLNAME = ''
       MODULE = ''
       MODULE_INDEX = ''
       if 'FPix' in line1:
          ROCNAMEALL = line1.split(' ')[1]
          MODULE = line1.split(' ')[1]
          FULLNAME =  MODULE.split('_ROC')[0]
          MODULE = MODULE.replace('_D','Z')
          MODULE = MODULE.split('Z')[1]
          MODULE = MODULE.replace('_BLD','-')
          MODULE = MODULE.replace('_PNL','-')
          MODULE = MODULE.replace('_RNG','-')
          ROC = MODULE.split('_ROC')[1]
          MODULE = MODULE.split('_ROC')[0]
          MODULE_INDEX = line1.split(' ')[2].strip()
          RNG = MODULE.split('-')[3]
          for line2 in INDATA_MOD2:
             if 'FPix' not in line2:
                if MODULE_INDEX == line2.split(' ')[0]:
                    if float(line2.split(' ')[1]) < 30. or float(line2.split(' ')[2]) < 30.:
                        if ROCNAMEALL not in tempModLow:
                            tempModLow.append(ROCNAMEALL)
                    if float(line2.split(' ')[4]) == 0 or float(line2.split(' ')[1]) == 0 or float(line2.split(' ')[2]) == 0:
                        if ROCNAMEALL not in tempModZero:
                            tempModZero.append(ROCNAMEALL)
                        badCount += 1
                        totalCount += 1
                    elif (float(line2.split(' ')[1]) > 255. or float(line2.split(' ')[2]) > 255. or float(line2.split(' ')[3]) > 255. or float(line2.split(' ')[4]) > 255.):
                        if ROCNAMEALL not in tempModHi:
                            tempModHi.append(ROCNAMEALL)
                        badCount += 1
                        totalCount += 1
                    elif (float(line2.split(' ')[1]) == float(line2.split(' ')[2]) and float(line2.split(' ')[2]) == float(line2.split(' ')[3]) and float(line2.split(' ')[3]) == float(line2.split(' ')[4])):
                        if ROCNAMEALL not in tempModIdent:
                            tempModIdent.append(ROCNAMEALL)
                        badCount += 1
                        totalCount += 1
                    else:
                        goodCount += 1
                        totalCount += 1
                        if ROCNAMEALL not in tempModUsed:
                            tempModUsed.append(ROCNAMEALL)
                        SUBLIST = [MODULE_INDEX,
                        FULLNAME,
                        MODULE,
                        ROC,
                        float(line2.split(' ')[1]),
                        float(line2.split(' ')[2]),
                        float(line2.split(' ')[3]),
                        float(line2.split(' ')[4]),
                        float(line2.split(' ')[5].replace('\n','')),
                        2.*(1.235)*(float(line2.split(' ')[1])/(float(line2.split(' ')[4]))),
                        2.*(1.235)*(float(line2.split(' ')[2])/(float(line2.split(' ')[4]))),
                        convertVbg(float(line2.split(' ')[4]),float(ROC),lumINDEX[M],int(RNG)),
                        returnDose(float(ROC),lumINDEX[M],int(RNG)),
                        2.*(1.235)*returnVbgShift(returnDose(float(ROC),lumINDEX[M],int(RNG)))*(float(line2.split(' ')[1])/(float(line2.split(' ')[4]))),
                        2.*(1.235)*returnVbgShift(returnDose(float(ROC),lumINDEX[M],int(RNG)))*(float(line2.split(' ')[2])/(float(line2.split(' ')[4]))),
                        correctADC(float(line2.split(' ')[1]),float(ROC),lumINDEX[M],int(RNG)),
                        correctADC(float(line2.split(' ')[2]),float(ROC),lumINDEX[M],int(RNG)),
                        correctADC(convertVbg(float(line2.split(' ')[4]),float(ROC),lumINDEX[M],int(RNG)),float(ROC),lumINDEX[M],int(RNG)),
                        (1/float(line2.split(' ')[1])) * correctADC(float(line2.split(' ')[1]),float(ROC),lumINDEX[M],int(RNG)),
                        (1/float(line2.split(' ')[2])) * correctADC(float(line2.split(' ')[2]),float(ROC),lumINDEX[M],int(RNG)),
                        (1/float(convertVbg(float(line2.split(' ')[4]),float(ROC),lumINDEX[M],int(RNG)))) * correctADC(convertVbg(float(line2.split(' ')[4]),float(ROC),lumINDEX[M],int(RNG)),float(ROC),lumINDEX[M],int(RNG))
                        ]
                        RB_ROC_LIST.append(SUBLIST)
                    break
          INDATA_MOD2.seek(0)

    DividoGram = TH1F("DividoGram", "threes", 8 ,0 ,8)
    for i in range (0,9):
        DividoGram.SetBinContent(i,3.)

    #print "  BAD ROC: " + str(badCount)
    #print " GOOD ROC: " + str(goodCount)
    #print "TOTAL ROC: " + str(totalCount)

    for m in tempModZero:
        print m + '  ADC Value = zero'
    for m in tempModIdent:
        print m + '  identical ADC values ( < 255)'
    for m in tempModHi:
        print m + '  ADC values identical and too high ( > 255)'
    for m in tempModUsed:
        print m + '  Valid'
    for m in tempModLow:
        print m + '  Low Va ADC( <30 )'

    p.cd()
    for ADC in ADCs:
        adc_Histo = TH1F(ADC+"HistoByLocation", ADC+"HistoByLocation", 10600 ,0 ,10600)
        print "ROC List Length: " + str(len(RB_ROC_LIST))
        for i in range(1,len(RB_ROC_LIST)):
            adc_Histo.SetBinContent(int(RB_ROC_LIST[i][0])+1,RB_ROC_LIST[i][ADCIndex[ADC]])
        adc_Histo.Write(ADC+"HistoByLocation")

    for VAL in abrevVALS:
        HistoCombROC_SumRNG1_Average = TH1F(VAL+"HistoCombROC_SumRNG1_Average", VAL+" Histogram RNG1 Average (Combined)", 8 ,0 ,8)
        HistoCombROC_SumRNG2_Average = TH1F(VAL+"HistoCombROC_SumRNG2_Average", VAL+" Histogram RNG2 Average (Combined)", 8 ,0 ,8)
        for DISK in DISKS:
            HistoROC_SumRNG1 = TH1F(VAL+"AllROCHisto_" + DISK + "RNG1", VAL+" Histogram " + DISK + " RNG1 Average", 16 ,0 ,16)
            HistoROC_SumRNG1.GetXaxis().SetTitle("ROC")
            HistoROC_SumRNG1.GetYaxis().SetTitle("[V]")

            HistoROC_SumRNG2 = TH1F(VAL+"AllROCHisto_" + DISK + "RNG2", VAL+" Histogram " + DISK + " RNG2 Average", 16 ,0 ,16)
            HistoROC_SumRNG2.GetXaxis().SetTitle("ROC")
            HistoROC_SumRNG2.GetYaxis().SetTitle("[V]")

            HistoCombROC_SumRNG1 = TH1F(VAL+"CombROCHisto_" + DISK + "RNG1", VAL+" Histogram " + DISK + " RNG1 Average (Combined)", 8 ,0 ,8)
            HistoCombROC_SumRNG1.GetXaxis().SetTitle("ROC")
            HistoCombROC_SumRNG1.GetYaxis().SetTitle("[V]")

            HistoCombROC_SumRNG2 = TH1F(VAL+"CombROCHisto_" + DISK + "RNG2", VAL+" Histogram " + DISK + " RNG2 Average (Combined)", 8 ,0 ,8)
            HistoCombROC_SumRNG2.GetXaxis().SetTitle("ROC")
            HistoCombROC_SumRNG2.GetYaxis().SetTitle("[V]")
            
            HistoROC_SumRNG1_DEN = TH1F(VAL+"AllROCHisto_" + DISK + "RNG1_DEN", VAL+" Histogram " + DISK + " RNG1_DEN Average", 16 ,0 ,16)
            HistoROC_SumRNG2_DEN = TH1F(VAL+"AllROCHisto_" + DISK + "RNG2_DEN", VAL+" Histogram " + DISK + " RNG2_DEN Average", 16 ,0 ,16)
            
            HistoCombROC_SumRNG1_DEN = TH1F(VAL+"CombROCHisto_" + DISK + "RNG1_DEN", VAL+" Histogram " + DISK + " RNG1_DEN Average (Combined)", 8 ,0 ,8)
            HistoCombROC_SumRNG2_DEN = TH1F(VAL+"CombROCHisto_" + DISK + "RNG2_DEN", VAL+" Histogram " + DISK + " RNG2_DEN Average (Combined)", 8 ,0 ,8)
            
            k = 0
            for i in range(1,len(RB_ROC_LIST)):
              if float(RB_ROC_LIST[i][4]) < 260. and float(RB_ROC_LIST[i][5]) < 260. and float(RB_ROC_LIST[i][6]) < 260. and float(RB_ROC_LIST[i][7]) < 260. and not (float(RB_ROC_LIST[i][4]) == float(RB_ROC_LIST[i][5]) and float(RB_ROC_LIST[i][5]) == float(RB_ROC_LIST[i][6]) and float(RB_ROC_LIST[i][6]) == float(RB_ROC_LIST[i][7])):
                  modTemp = RB_ROC_LIST[i][2]
                  fullNameTemp = RB_ROC_LIST[i][1]
                  if fullNameTemp.split('_')[5]=='RNG1':
                    if fullNameTemp.split('_')[2]==('D' + DISK):
                        HistoROC_SumRNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][valINDEX[VAL]])
                        HistoROC_SumRNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
                        HistoCombROC_SumRNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][valINDEX[VAL]])
                        HistoCombROC_SumRNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
                  if fullNameTemp.split('_')[5]=='RNG2':
                    if fullNameTemp.split('_')[2]==('D' + DISK):
                        HistoROC_SumRNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][valINDEX[VAL]])
                        HistoROC_SumRNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
                        HistoCombROC_SumRNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][valINDEX[VAL]])
                        HistoCombROC_SumRNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            #Vd
            HistoROC_SumRNG1.Divide(HistoROC_SumRNG1_DEN)
            HistoROC_SumRNG2.Divide(HistoROC_SumRNG2_DEN)
            HistoCombROC_SumRNG1.Divide(HistoCombROC_SumRNG1_DEN)
            HistoCombROC_SumRNG2.Divide(HistoCombROC_SumRNG2_DEN)
            
            HistoROC_SumRNG1.Write(VAL+"HistoROC_Sum" + DISK + "RNG1")
            HistoROC_SumRNG2.Write(VAL+"HistoROC_Sum" + DISK + "RNG2")
            HistoCombROC_SumRNG1.Write(VAL+"HistoCombROC_Sum" + DISK + "RNG1")
            HistoCombROC_SumRNG2.Write(VAL+"HistoCombROC_Sum" + DISK + "RNG2")
            HistoCombROC_SumRNG1_Average.Add(HistoCombROC_SumRNG1)
            HistoCombROC_SumRNG2_Average.Add(HistoCombROC_SumRNG2)

        HistoCombROC_SumRNG1_Average.Divide(DividoGram)
        HistoCombROC_SumRNG2_Average.Divide(DividoGram)

        HistoCombROC_SumRNG1_Average.Write(VAL+"CombROC_RNG1_Average")
        HistoCombROC_SumRNG2_Average.Write(VAL+"CombROC_RNG2_Average")

    p.Close()
    INDATA_MOD1.close()
    INDATA_MOD2.close()
