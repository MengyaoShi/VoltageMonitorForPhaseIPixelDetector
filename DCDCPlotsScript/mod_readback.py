#!/user/local/bin/python
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

p = TFile("plots.root", "recreate")

READBACKER_MOD = sys.argv[1]
CSV_DCDC = sys.argv[2]
READBACKER_MAP = sys.argv[3]
CSV_DCU = sys.argv[4]

INDATA_MOD1 = open(READBACKER_MOD)
INDATA_MOD2 = open(READBACKER_MOD)
INDATA_MAP = open(READBACKER_MAP) 
INDATA_DCDC = open(CSV_DCDC)
INDATA_DCU = open(CSV_DCU)

OUTDATA = open('out.csv', 'w')

topLine = ''
for line in INDATA_DCU:
    if 'Official.name.of.position' in line:
        topLine = line.rstrip('\n') + ',VdDCU(V),VaDCU(V)' + '\n'
        OUTDATA.write(topLine)
INDATA_DCU.seek(0)

def DCDC_MAP (X,Y):
   add=1
   if X=='T':
      add += 4
   if (int(Y) % 2 != 0):
      add += 2
   return add

#CREATE ROC LIST
RB_ROC_LIST = []
for line1 in INDATA_MOD1:
   FULLNAME = ''
   MODULE = ''
   MODULE_INDEX = ''
   PC = ''
   PCL = ''
   PN = ''
   VA_DCDC = -999.0
   VD_DCDC = -999.0
   if 'FPix' in line1:
      MODULE = line1.split(' ')[1]
      FULLNAME =  MODULE.split('_ROC')[0]
      for line4 in INDATA_MAP:
       if 'FPix' in line4:
          if line4.split(',')[0].split('_D')[1] == FULLNAME.split('_D')[1]:
                PC = line4.split(',')[1][0] + line4.split(',')[1][2].upper()
                PCL = line4.split(',')[1][1].upper()
                PN = line4.split(',')[2].split('\r')[0]
      INDATA_MAP.seek(0)
      for line5 in INDATA_DCDC:
         if PC == line5.split(',')[0]:
            VA_DCDC = line5.split(',')[DCDC_MAP (PCL,PN)]
            VD_DCDC = line5.split(',')[DCDC_MAP (PCL,PN)+1]
      INDATA_DCDC.seek(0)
      MODULE = MODULE.replace('_D','Z')
      MODULE = MODULE.split('Z')[1]
      MODULE = MODULE.replace('_BLD','-')
      MODULE = MODULE.replace('_PNL','-')
      MODULE = MODULE.replace('_RNG','-')
      ROC = MODULE.split('_ROC')[1]
      MODULE = MODULE.split('_ROC')[0]
      MODULE_INDEX = line1.split(' ')[2].strip()
      for line2 in INDATA_MOD2:
         if 'FPix' not in line2:
            if MODULE_INDEX == line2.split(' ')[0]:
               SUBLIST = [MODULE_INDEX,FULLNAME,MODULE,ROC,PC,PCL,int(PN),float(line2.split(' ')[1]),float(line2.split(' ')[2]),float(line2.split(' ')[3]),float(line2.split(' ')[4]),float(line2.split(' ')[5].replace('\n','')),2*(1.235)*(float(line2.split(' ')[1])/float(line2.split(' ')[4])),2*(1.235)*(float(line2.split(' ')[2])/float(line2.split(' ')[4])), float(VD_DCDC.split('\r')[0]), float(VA_DCDC)]
               RB_ROC_LIST.append(SUBLIST)
               break
      INDATA_MOD2.seek(0)

#for i in range (0,len(RB_ROC_LIST)):
#   print RB_ROC_LIST[i]

#CREATE MODULE LIST
RB_MOD_LIST = []
modTemp = ''
for i in range(1,len(RB_ROC_LIST)):
   if RB_ROC_LIST[i][2] != modTemp:
      disconCheck = 0
      Vd = 0.
      Va = 0.
      c = 0.
      VdDCU = 0.
      VaDCU = 0.
      modTemp = RB_ROC_LIST[i][2]
      fullNameTemp = RB_ROC_LIST[i][1]
      PC = RB_ROC_LIST[i][4]
      PCL = RB_ROC_LIST[i][5]
      PN = RB_ROC_LIST[i][6]
      VdDCDC = RB_ROC_LIST[i][14]
      VaDCDC = RB_ROC_LIST[i][15]
      for j in range(i,len(RB_ROC_LIST)):
         if RB_ROC_LIST[j][2] == modTemp:
            if float(RB_ROC_LIST[j][7]) > 300:
               disconCheck = 1
            Vd += RB_ROC_LIST[j][12]
            Va += RB_ROC_LIST[j][13]
            c += 1.
      Vd = Vd/c
      Va = Va/c
      for line in INDATA_DCU:
        if (fullNameTemp + '_ROC0') == line.split(',')[2]:
            VdDCU = line.split(',')[36]
            VaDCU = line.split(',')[34]
            newline = line.rstrip('\n') +','+ str(VdDCDC) +','+ str(VaDCDC) + '\n'
            OUTDATA.write(newline)
      INDATA_DCU.seek(0)
      tempEntry = [fullNameTemp,modTemp,PC,PCL,PN,Vd,Va,VdDCDC,VaDCDC,VdDCDC-Vd,VaDCDC-Va,VdDCU,VaDCU]
      if disconCheck == 0 and tempEntry[11] != 'NA':
         RB_MOD_LIST.append(tempEntry)
      else:
         print 'Module ' + modTemp + ' values unphysical, likely disconnected'

for i in range (0,len(RB_MOD_LIST)):
   print RB_MOD_LIST[i]

INDATA_MOD1.close()
INDATA_MOD2.close()
INDATA_MAP.close()
INDATA_DCDC.close()
INDATA_DCU.close()

OUTDATA.close()

VdHisto = TH1D("VdHisto", "Vd Histogram", 50 ,2 ,4)
VaHisto = TH1D("VaHisto", "Va Histogram", 50 ,1 ,3)
VdAvgHisto = TH1D("VdAvgHisto", "Vd Module Avg Histogram", 100 ,2 ,4)
VaAvgHisto = TH1D("VaAvgHisto", "Va Module Avg Histogram", 100 ,1 ,3)

X = np.zeros(len(RB_MOD_LIST))
Y_Vd = np.zeros(len(RB_MOD_LIST))
Y_Va = np.zeros(len(RB_MOD_LIST))
Y_VdDCDC = np.zeros(len(RB_MOD_LIST))
Y_VaDCDC = np.zeros(len(RB_MOD_LIST))
Y_VdDiff = np.zeros(len(RB_MOD_LIST))
Y_VaDiff = np.zeros(len(RB_MOD_LIST))
Y_VdDCU = np.zeros(len(RB_MOD_LIST))
Y_VaDCU = np.zeros(len(RB_MOD_LIST))

for i in range(0,len(RB_MOD_LIST)):
   X[i] = i
   Y_Vd[i] = RB_MOD_LIST[i][5]
   Y_Va[i] = RB_MOD_LIST[i][6]
   Y_VdDCDC[i] = RB_MOD_LIST[i][7]
   Y_VaDCDC[i] = RB_MOD_LIST[i][8]
   Y_VdDiff[i] = RB_MOD_LIST[i][9]
   Y_VaDiff[i] = RB_MOD_LIST[i][10]
   Y_VdDCU[i] = RB_MOD_LIST[i][11]
   Y_VaDCU[i] = RB_MOD_LIST[i][12]

VdPlot = TGraph(len(RB_MOD_LIST), X, Y_Vd)
VaPlot = TGraph(len(RB_MOD_LIST), X, Y_Va)
VdDCDCPlot = TGraph(len(RB_MOD_LIST), X, Y_VdDCDC)
VaDCDCPlot = TGraph(len(RB_MOD_LIST), X, Y_VaDCDC)
VdDiffPlot = TGraph(len(RB_MOD_LIST), X, Y_VdDiff) 
VaDiffPlot = TGraph(len(RB_MOD_LIST), X, Y_VaDiff)
VdDCUPlot = TGraph(len(RB_MOD_LIST), X, Y_VdDCU)
VaDCUPlot = TGraph(len(RB_MOD_LIST), X, Y_VaDCU)

VdPlot.GetYaxis().SetRangeUser(0,3.75)
VaPlot.GetYaxis().SetRangeUser(0,3.0)
VdDCDCPlot.GetYaxis().SetRangeUser(0,3.75)
VaDCDCPlot.GetYaxis().SetRangeUser(0,3.0)

VdDiffPlot = TGraph(len(RB_MOD_LIST), X, Y_VdDiff)
VaDiffPlot = TGraph(len(RB_MOD_LIST), X, Y_VaDiff)


#FILL HISTOGRAMS
for i in range(1,len(RB_ROC_LIST)):
   if float(RB_ROC_LIST[i][7]) < 300:
      VdHisto.Fill(RB_ROC_LIST[i][12])
      VaHisto.Fill(RB_ROC_LIST[i][13])
   else:
      print 'ROC ' + RB_ROC_LIST[i][3] + ' ' + RB_ROC_LIST[i][1] + ' unphysical, disconnected'

for i in range(0,len(RB_MOD_LIST)):
   VdAvgHisto.Fill(RB_MOD_LIST[i][5])
   if float(RB_MOD_LIST[i][5]) < 2.8:
      print 'Vd Outlier Module ' + RB_MOD_LIST[i][1] + '   Vd = ' + str(RB_MOD_LIST[i][5]) 
   VaAvgHisto.Fill(RB_MOD_LIST[i][6])
   if float(RB_MOD_LIST[i][6]) < 1.85:
      print 'Va Outlier Module ' + RB_MOD_LIST[i][1] + '   Va = ' + str(RB_MOD_LIST[i][6])

p.cd()
VdHisto.Write("Vd")
VaHisto.Write("Va")
VdAvgHisto.Write("VdAvg")
VaAvgHisto.Write("VaAvg")
VdPlot.Write("VdPlot")
VaPlot.Write("VaPlot")
VdDCDCPlot.Write("VdDCDCPlot")
VaDCDCPlot.Write("VaDCDCPlot")
VdDiffPlot.Write("VdDiffPlot")
VaDiffPlot.Write("VaDiffPlot")
VdDCUPlot.Write("VdDCUPlot")
VaDCUPlot.Write("VaDCUPlot")
p.Close()

