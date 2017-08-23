#!/user/local/bin/python
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

gStyle.SetOptStat(0)

p = TFile("plots.root", "recreate")

READBACKER_MOD = sys.argv[1]

INDATA_MOD1 = open(READBACKER_MOD)
INDATA_MOD2 = open(READBACKER_MOD)

OUTDATA = open('out.csv', 'w')

topLine = ''

def returnCombROC(roc):
    if roc < 8:
        return roc
    else:
        return (15 - roc)

#CREATE ROC LIST
RB_ROC_LIST = []
for line1 in INDATA_MOD1:
   FULLNAME = ''
   MODULE = ''
   MODULE_INDEX = ''
   if 'FPix' in line1:
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
      for line2 in INDATA_MOD2:
         if 'FPix' not in line2:
            if MODULE_INDEX == line2.split(' ')[0]:
                if float(line2.split(' ')[4]) == 0:
                    print FULLNAME + ' ROC ' + ROC + '   Vbg = 0, ROC disconnected'
                else:
                    SUBLIST = [MODULE_INDEX,FULLNAME,MODULE,ROC,float(line2.split(' ')[1]),float(line2.split(' ')[2]),float(line2.split(' ')[3]),float(line2.split(' ')[4]),float(line2.split(' ')[5].replace('\n','')),2.*(1.235)*(float(line2.split(' ')[1])/float(line2.split(' ')[4])),2.*(1.235)*(float(line2.split(' ')[2])/float(line2.split(' ')[4]))]
                    RB_ROC_LIST.append(SUBLIST)
                break
      INDATA_MOD2.seek(0)

#Vd
VdHistoROC_SumD1RNG1 = TH1F("VdAllROCHisto_D1RNG1", "Vd Histogram D1 RNG1 Average", 16 ,0 ,16)
VdHistoROC_SumD1RNG1.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD1RNG1.GetYaxis().SetTitle("[V]")
VdHistoROC_SumD2RNG1 = TH1F("VdAllROCHisto_D2RNG1", "Vd Histogram D2 RNG1 Average", 16 ,0 ,16)
VdHistoROC_SumD2RNG1.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD2RNG1.GetYaxis().SetTitle("[V]")
VdHistoROC_SumD3RNG1 = TH1F("VdAllROCHisto_D3RNG1", "Vd Histogram D3 RNG1 Average", 16 ,0 ,16)
VdHistoROC_SumD3RNG1.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD3RNG1.GetYaxis().SetTitle("[V]")

VdHistoROC_SumD1RNG2 = TH1F("VdAllROCHisto_D1RNG2", "Vd Histogram D1 RNG2 Average", 16 ,0 ,16)
VdHistoROC_SumD1RNG2.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD1RNG2.GetYaxis().SetTitle("[V]")
VdHistoROC_SumD2RNG2 = TH1F("VdAllROCHisto_D2RNG2", "Vd Histogram D2 RNG2 Average", 16 ,0 ,16)
VdHistoROC_SumD2RNG2.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD2RNG2.GetYaxis().SetTitle("[V]")
VdHistoROC_SumD3RNG2 = TH1F("VdAllROCHisto_D3RNG2", "Vd Histogram D3 RNG2 Average", 16 ,0 ,16)
VdHistoROC_SumD3RNG2.GetXaxis().SetTitle("ROC")
VdHistoROC_SumD3RNG2.GetYaxis().SetTitle("[V]")

VdHistoCombROC_SumD1RNG1 = TH1F("VdCombROCHisto_D1RNG1", "Vd Histogram D1 RNG1 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD1RNG1.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD1RNG1.GetYaxis().SetTitle("[V]")
VdHistoCombROC_SumD2RNG1 = TH1F("VdCombROCHisto_D2RNG1", "Vd Histogram D2 RNG1 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD2RNG1.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD2RNG1.GetYaxis().SetTitle("[V]")
VdHistoCombROC_SumD3RNG1 = TH1F("VdCombROCHisto_D3RNG1", "Vd Histogram D3 RNG1 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD3RNG1.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD3RNG1.GetYaxis().SetTitle("[V]")

VdHistoCombROC_SumD1RNG2 = TH1F("VdCombROCHisto_D1RNG2", "Vd Histogram D1 RNG2 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD1RNG2.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD1RNG2.GetYaxis().SetTitle("[V]")
VdHistoCombROC_SumD2RNG2 = TH1F("VdCombROCHisto_D2RNG2", "Vd Histogram D2 RNG2 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD2RNG2.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD2RNG2.GetYaxis().SetTitle("[V]")
VdHistoCombROC_SumD3RNG2 = TH1F("VdCombROCHisto_D3RNG2", "Vd Histogram D3 RNG2 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD3RNG2.GetXaxis().SetTitle("ROC")
VdHistoCombROC_SumD3RNG2.GetYaxis().SetTitle("[V]")

#Va

VaHistoROC_SumD1RNG1 = TH1F("VaAllROCHisto_D1RNG1", "Va Histogram D1 RNG1 Average", 16 ,0 ,16)
VaHistoROC_SumD1RNG1.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD1RNG1.GetYaxis().SetTitle("[V]")
VaHistoROC_SumD2RNG1 = TH1F("VaAllROCHisto_D2RNG1", "Va Histogram D2 RNG1 Average", 16 ,0 ,16)
VaHistoROC_SumD2RNG1.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD2RNG1.GetYaxis().SetTitle("[V]")
VaHistoROC_SumD3RNG1 = TH1F("VaAllROCHisto_D3RNG1", "Va Histogram D3 RNG1 Average", 16 ,0 ,16)
VaHistoROC_SumD3RNG1.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD3RNG1.GetYaxis().SetTitle("[V]")

VaHistoROC_SumD1RNG2 = TH1F("VaAllROCHisto_D1RNG2", "Va Histogram D1 RNG2 Average", 16 ,0 ,16)
VaHistoROC_SumD1RNG2.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD1RNG2.GetYaxis().SetTitle("[V]")
VaHistoROC_SumD2RNG2 = TH1F("VaAllROCHisto_D2RNG2", "Va Histogram D2 RNG2 Average", 16 ,0 ,16)
VaHistoROC_SumD2RNG2.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD2RNG2.GetYaxis().SetTitle("[V]")
VaHistoROC_SumD3RNG2 = TH1F("VaAllROCHisto_D3RNG2", "Va Histogram D3 RNG2 Average", 16 ,0 ,16)
VaHistoROC_SumD3RNG2.GetXaxis().SetTitle("ROC")
VaHistoROC_SumD3RNG2.GetYaxis().SetTitle("[V]")

VaHistoCombROC_SumD1RNG1 = TH1F("VaCombROCHisto_D1RNG1", "Va Histogram D1 RNG1 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD1RNG1.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD1RNG1.GetYaxis().SetTitle("[V]")
VaHistoCombROC_SumD2RNG1 = TH1F("VaCombROCHisto_D2RNG1", "Va Histogram D2 RNG1 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD2RNG1.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD2RNG1.GetYaxis().SetTitle("[V]")
VaHistoCombROC_SumD3RNG1 = TH1F("VaCombROCHisto_D3RNG1", "Va Histogram D3 RNG1 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD3RNG1.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD3RNG1.GetYaxis().SetTitle("[V]")

VaHistoCombROC_SumD1RNG2 = TH1F("VaCombROCHisto_D1RNG2", "Va Histogram D1 RNG2 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD1RNG2.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD1RNG2.GetYaxis().SetTitle("[V]")
VaHistoCombROC_SumD2RNG2 = TH1F("VaCombROCHisto_D2RNG2", "Va Histogram D2 RNG2 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD2RNG2.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD2RNG2.GetYaxis().SetTitle("[V]")
VaHistoCombROC_SumD3RNG2 = TH1F("VaCombROCHisto_D3RNG2", "Va Histogram D3 RNG2 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD3RNG2.GetXaxis().SetTitle("ROC")
VaHistoCombROC_SumD3RNG2.GetYaxis().SetTitle("[V]")

#AVG
VdHistoCombROC_SumRNG1 = TH1F("VdHistoCombROC_SumRNG1", "Vd Histogram RNG1 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumRNG1 = TH1F("VaHistoCombROC_SumRNG1", "Va Histogram RNG1 Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumRNG2 = TH1F("VdHistoCombROC_SumRNG2", "Vd Histogram RNG2 Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumRNG2 = TH1F("VaHistoCombROC_SumRNG2", "Va Histogram RNG2 Average (Combined)", 8 ,0 ,8)

#Denominator Histos

VdHistoROC_SumD1RNG1_DEN = TH1F("VdAllROCHisto_D1RNG1_DEN", "Vd Histogram D1 RNG1_DEN Average", 16 ,0 ,16)
VdHistoROC_SumD2RNG1_DEN = TH1F("VdAllROCHisto_D2RNG1_DEN", "Vd Histogram D2 RNG1_DEN Average", 16 ,0 ,16)
VdHistoROC_SumD3RNG1_DEN = TH1F("VdAllROCHisto_D3RNG1_DEN", "Vd Histogram D3 RNG1_DEN Average", 16 ,0 ,16)

VdHistoROC_SumD1RNG2_DEN = TH1F("VdAllROCHisto_D1RNG2_DEN", "Vd Histogram D1 RNG2_DEN Average", 16 ,0 ,16)
VdHistoROC_SumD2RNG2_DEN = TH1F("VdAllROCHisto_D2RNG2_DEN", "Vd Histogram D2 RNG2_DEN Average", 16 ,0 ,16)
VdHistoROC_SumD3RNG2_DEN = TH1F("VdAllROCHisto_D3RNG2_DEN", "Vd Histogram D3 RNG2_DEN Average", 16 ,0 ,16)

VdHistoCombROC_SumD1RNG1_DEN = TH1F("VdCombROCHisto_D1RNG1_DEN", "Vd Histogram D1 RNG1_DEN Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD2RNG1_DEN = TH1F("VdCombROCHisto_D2RNG1_DEN", "Vd Histogram D2 RNG1_DEN Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD3RNG1_DEN = TH1F("VdCombROCHisto_D3RNG1_DEN", "Vd Histogram D3 RNG1_DEN Average (Combined)", 8 ,0 ,8)

VdHistoCombROC_SumD1RNG2_DEN = TH1F("VdCombROCHisto_D1RNG2_DEN", "Vd Histogram D1 RNG2_DEN Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD2RNG2_DEN = TH1F("VdCombROCHisto_D2RNG2_DEN", "Vd Histogram D2 RNG2_DEN Average (Combined)", 8 ,0 ,8)
VdHistoCombROC_SumD3RNG2_DEN = TH1F("VdCombROCHisto_D3RNG2_DEN", "Vd Histogram D3 RNG2_DEN Average (Combined)", 8 ,0 ,8)

#Va

VaHistoROC_SumD1RNG1_DEN = TH1F("VaAllROCHisto_D1RNG1_DEN", "Va Histogram D1 RNG1_DEN Average", 16 ,0 ,16)
VaHistoROC_SumD2RNG1_DEN = TH1F("VaAllROCHisto_D2RNG1_DEN", "Va Histogram D2 RNG1_DEN Average", 16 ,0 ,16)
VaHistoROC_SumD3RNG1_DEN = TH1F("VaAllROCHisto_D3RNG1_DEN", "Va Histogram D3 RNG1_DEN Average", 16 ,0 ,16)

VaHistoROC_SumD1RNG2_DEN = TH1F("VaAllROCHisto_D1RNG2_DEN", "Va Histogram D1 RNG2_DEN Average", 16 ,0 ,16)
VaHistoROC_SumD2RNG2_DEN = TH1F("VaAllROCHisto_D2RNG2_DEN", "Va Histogram D2 RNG2_DEN Average", 16 ,0 ,16)
VaHistoROC_SumD3RNG2_DEN = TH1F("VaAllROCHisto_D3RNG2_DEN", "Va Histogram D3 RNG2_DEN Average", 16 ,0 ,16)

VaHistoCombROC_SumD1RNG1_DEN = TH1F("VaCombROCHisto_D1RNG1_DEN", "Va Histogram D1 RNG1_DEN Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD2RNG1_DEN = TH1F("VaCombROCHisto_D2RNG1_DEN", "Va Histogram D2 RNG1_DEN Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD3RNG1_DEN = TH1F("VaCombROCHisto_D3RNG1_DEN", "Va Histogram D3 RNG1_DEN Average (Combined)", 8 ,0 ,8)

VaHistoCombROC_SumD1RNG2_DEN = TH1F("VaCombROCHisto_D1RNG2_DEN", "Va Histogram D1 RNG2_DEN Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD2RNG2_DEN = TH1F("VaCombROCHisto_D2RNG2_DEN", "Va Histogram D2 RNG2_DEN Average (Combined)", 8 ,0 ,8)
VaHistoCombROC_SumD3RNG2_DEN = TH1F("VaCombROCHisto_D3RNG2_DEN", "Va Histogram D3 RNG2_DEN Average (Combined)", 8 ,0 ,8)

k = 0
for i in range(1,len(RB_ROC_LIST)):
  if float(RB_ROC_LIST[i][4]) < 260:
      modTemp = RB_ROC_LIST[i][2]
      fullNameTemp = RB_ROC_LIST[i][1]
      if fullNameTemp.split('_')[5]=='RNG1':
        if fullNameTemp.split('_')[2]=='D1':
            VdHistoROC_SumD1RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD1RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD1RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD1RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD1RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD1RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD1RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD1RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
        if fullNameTemp.split('_')[2]=='D2':
            VdHistoROC_SumD2RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD2RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD2RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD2RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD2RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD2RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD2RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD2RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
        if fullNameTemp.split('_')[2]=='D3':
            VdHistoROC_SumD3RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD3RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD3RNG1.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD3RNG1_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD3RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD3RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD3RNG1.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD3RNG1_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
      if fullNameTemp.split('_')[5]=='RNG2':
        if fullNameTemp.split('_')[2]=='D1':
            VdHistoROC_SumD1RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD1RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD1RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD1RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD1RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD1RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD1RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD1RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
        if fullNameTemp.split('_')[2]=='D2':
            VdHistoROC_SumD2RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD2RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD2RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD2RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD2RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD2RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD2RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD2RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
        if fullNameTemp.split('_')[2]=='D3':
            VdHistoROC_SumD3RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][9])
            VdHistoROC_SumD3RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VaHistoROC_SumD3RNG2.AddBinContent(int(RB_ROC_LIST[i][3])+1,RB_ROC_LIST[i][10])
            VaHistoROC_SumD3RNG2_DEN.AddBinContent(int(RB_ROC_LIST[i][3])+1,1.0)
            VdHistoCombROC_SumD3RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][9])
            VdHistoCombROC_SumD3RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)
            VaHistoCombROC_SumD3RNG2.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,RB_ROC_LIST[i][10])
            VaHistoCombROC_SumD3RNG2_DEN.AddBinContent(returnCombROC(int(RB_ROC_LIST[i][3]))+1,1.0)

#Vd
VdHistoROC_SumD1RNG1.Divide(VdHistoROC_SumD1RNG1_DEN)
VdHistoROC_SumD2RNG1.Divide(VdHistoROC_SumD2RNG1_DEN)
VdHistoROC_SumD3RNG1.Divide(VdHistoROC_SumD3RNG1_DEN)

VdHistoROC_SumD1RNG2.Divide(VdHistoROC_SumD1RNG2_DEN)
VdHistoROC_SumD2RNG2.Divide(VdHistoROC_SumD2RNG2_DEN)
VdHistoROC_SumD3RNG2.Divide(VdHistoROC_SumD3RNG2_DEN)

VdHistoCombROC_SumD1RNG1.Divide(VdHistoCombROC_SumD1RNG1_DEN)
VdHistoCombROC_SumD2RNG1.Divide(VdHistoCombROC_SumD2RNG1_DEN)
VdHistoCombROC_SumD3RNG1.Divide(VdHistoCombROC_SumD3RNG1_DEN)

VdHistoCombROC_SumD1RNG2.Divide(VdHistoCombROC_SumD1RNG2_DEN)
VdHistoCombROC_SumD2RNG2.Divide(VdHistoCombROC_SumD2RNG2_DEN)
VdHistoCombROC_SumD3RNG2.Divide(VdHistoCombROC_SumD3RNG2_DEN)

#Va
VaHistoROC_SumD1RNG1.Divide(VaHistoROC_SumD1RNG1_DEN)
VaHistoROC_SumD2RNG1.Divide(VaHistoROC_SumD2RNG1_DEN)
VaHistoROC_SumD3RNG1.Divide(VaHistoROC_SumD3RNG1_DEN)

VaHistoROC_SumD1RNG2.Divide(VaHistoROC_SumD1RNG2_DEN)
VaHistoROC_SumD2RNG2.Divide(VaHistoROC_SumD2RNG2_DEN)
VaHistoROC_SumD3RNG2.Divide(VaHistoROC_SumD3RNG2_DEN)

VaHistoCombROC_SumD1RNG1.Divide(VaHistoCombROC_SumD1RNG1_DEN)
VaHistoCombROC_SumD2RNG1.Divide(VaHistoCombROC_SumD2RNG1_DEN)
VaHistoCombROC_SumD3RNG1.Divide(VaHistoCombROC_SumD3RNG1_DEN)

VaHistoCombROC_SumD1RNG2.Divide(VaHistoCombROC_SumD1RNG2_DEN)
VaHistoCombROC_SumD2RNG2.Divide(VaHistoCombROC_SumD2RNG2_DEN)
VaHistoCombROC_SumD3RNG2.Divide(VaHistoCombROC_SumD3RNG2_DEN)


DividoGram = TH1F("DividoGram", "threes", 8 ,0 ,8)
for i in range (0,9):
    DividoGram.SetBinContent(i,3.)
#adding AVG of rng histos
VdHistoCombROC_SumRNG1.Add(VdHistoCombROC_SumD1RNG1)
VdHistoCombROC_SumRNG1.Add(VdHistoCombROC_SumD2RNG1)
VdHistoCombROC_SumRNG1.Add(VdHistoCombROC_SumD3RNG1)
VdHistoCombROC_SumRNG1.Divide(DividoGram)

VaHistoCombROC_SumRNG1.Add(VaHistoCombROC_SumD1RNG1)
VaHistoCombROC_SumRNG1.Add(VaHistoCombROC_SumD2RNG1)
VaHistoCombROC_SumRNG1.Add(VaHistoCombROC_SumD3RNG1)
VaHistoCombROC_SumRNG1.Divide(DividoGram)

VdHistoCombROC_SumRNG2.Add(VdHistoCombROC_SumD1RNG2)
VdHistoCombROC_SumRNG2.Add(VdHistoCombROC_SumD2RNG2)
VdHistoCombROC_SumRNG2.Add(VdHistoCombROC_SumD3RNG2)
VdHistoCombROC_SumRNG2.Divide(DividoGram)

VaHistoCombROC_SumRNG2.Add(VaHistoCombROC_SumD1RNG2)
VaHistoCombROC_SumRNG2.Add(VaHistoCombROC_SumD2RNG2)
VaHistoCombROC_SumRNG2.Add(VaHistoCombROC_SumD3RNG2)
VaHistoCombROC_SumRNG2.Divide(DividoGram)

p.cd()
VdHistoROC_SumD1RNG1.Write("VdHistoROC_SumD1RNG1")
VdHistoROC_SumD2RNG1.Write("VdHistoROC_SumD2RNG1")
VdHistoROC_SumD3RNG1.Write("VdHistoROC_SumD3RNG1")
VdHistoROC_SumD1RNG2.Write("VdHistoROC_SumD1RNG2")
VdHistoROC_SumD2RNG2.Write("VdHistoROC_SumD2RNG2")
VdHistoROC_SumD3RNG2.Write("VdHistoROC_SumD3RNG2")
VdHistoCombROC_SumD1RNG1.Write("VdHistoCombROC_SumD1RNG1")
VdHistoCombROC_SumD2RNG1.Write("VdHistoCombROC_SumD2RNG1")
VdHistoCombROC_SumD3RNG1.Write("VdHistoCombROC_SumD3RNG1")
VdHistoCombROC_SumD1RNG2.Write("VdHistoCombROC_SumD1RNG2")
VdHistoCombROC_SumD2RNG2.Write("VdHistoCombROC_SumD2RNG2")
VdHistoCombROC_SumD3RNG2.Write("VdHistoCombROC_SumD3RNG2")
VaHistoROC_SumD1RNG1.Write("VaHistoROC_SumD1RNG1")
VaHistoROC_SumD2RNG1.Write("VaHistoROC_SumD2RNG1")
VaHistoROC_SumD3RNG1.Write("VaHistoROC_SumD3RNG1")
VaHistoROC_SumD1RNG2.Write("VaHistoROC_SumD1RNG2")
VaHistoROC_SumD2RNG2.Write("VaHistoROC_SumD2RNG2")
VaHistoROC_SumD3RNG2.Write("VaHistoROC_SumD3RNG2")
VaHistoCombROC_SumD1RNG1.Write("VaHistoCombROC_SumD1RNG1")
VaHistoCombROC_SumD2RNG1.Write("VaHistoCombROC_SumD2RNG1")
VaHistoCombROC_SumD3RNG1.Write("VaHistoCombROC_SumD3RNG1")
VaHistoCombROC_SumD1RNG2.Write("VaHistoCombROC_SumD1RNG2")
VaHistoCombROC_SumD2RNG2.Write("VaHistoCombROC_SumD2RNG2")
VaHistoCombROC_SumD3RNG2.Write("VaHistoCombROC_SumD3RNG2")

VdHistoCombROC_SumRNG1.Write("VdCombROC_RNG1_Average")

VaHistoCombROC_SumRNG1.Write("VaCombROC_RNG1_Average")

VdHistoCombROC_SumRNG2.Write("VdCombROC_RNG2_Average")

VaHistoCombROC_SumRNG2.Write("VaCombROC_RNG2_Average")

p.Close()
