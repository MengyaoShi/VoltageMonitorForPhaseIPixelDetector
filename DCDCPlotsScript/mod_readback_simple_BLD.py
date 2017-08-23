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

INDATA_MOD1 = open(READBACKER_MOD)
INDATA_MOD2 = open(READBACKER_MOD)

OUTDATA = open('out.csv', 'w')

topLine = ''

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

#CREATE MODULE LIST
RB_MOD_LIST = []
fullNameTemp = ''
modTemp = ''
for i in range(1,len(RB_ROC_LIST)):
   if RB_ROC_LIST[i][1] != fullNameTemp:
      disconCheck = 0
      Vd = 0.
      Va = 0.
      c = 0.
      modTemp = RB_ROC_LIST[i][2]
      fullNameTemp = RB_ROC_LIST[i][1]
      modIndex = RB_ROC_LIST[i][0]
      for j in range(i,len(RB_ROC_LIST)):
         if RB_ROC_LIST[j][1] == fullNameTemp:
            if float(RB_ROC_LIST[j][4]) > 260:
               print 'found bad value for ' + fullNameTemp + '    Vbg: ' +str(float(RB_ROC_LIST[j][4]))
            else:
               Vd += RB_ROC_LIST[j][9]
               Va += RB_ROC_LIST[j][10]
               c += 1.
      if c != 0.:
        Vd = Vd/c
        Va = Va/c
      else:
        Vd = 0.
        Va = 0.
      tempEntry = [fullNameTemp,modTemp,Vd,Va,modIndex]
      RB_MOD_LIST.append(tempEntry)

#for i in range (0,len(RB_MOD_LIST)):
#   print str(i) +  '   ' + str(RB_MOD_LIST[i])

INDATA_MOD1.close()
INDATA_MOD2.close()

OUTDATA.close()

VdHisto = TH1D("VdHisto", "Vd Histogram", 50 ,2 ,4)
VaHisto = TH1D("VaHisto", "Va Histogram", 50 ,1 ,3)
VdAvgHisto = TH1D("VdAvgHisto", "Vd Module Avg Histogram", 100 ,2 ,4)
VaAvgHisto = TH1D("VaAvgHisto", "Va Module Avg Histogram", 100 ,1 ,3)

X = np.zeros(len(RB_MOD_LIST))
Y_Vd = np.zeros(len(RB_MOD_LIST))
Y_Va = np.zeros(len(RB_MOD_LIST))

for i in range(0,len(RB_MOD_LIST)):
   X[i] = i
   Y_Vd[i] = RB_MOD_LIST[i][2]
   Y_Va[i] = RB_MOD_LIST[i][3]

VdPlot = TGraph(len(RB_MOD_LIST), X, Y_Vd)
VaPlot = TGraph(len(RB_MOD_LIST), X, Y_Va)

VdPlot.GetYaxis().SetRangeUser(0,3.75)
VaPlot.GetYaxis().SetRangeUser(0,3.0)

#FILL HISTOGRAMS
for i in range(1,len(RB_ROC_LIST)):
   if float(RB_ROC_LIST[i][4]) < 260:
      VdHisto.Fill(RB_ROC_LIST[i][9])
      VaHisto.Fill(RB_ROC_LIST[i][10])
   else:
      print RB_ROC_LIST[i][1] + ' ROC ' + RB_ROC_LIST[i][3] + ' values unphysical, disconnected'

for i in range(0,len(RB_MOD_LIST)):
   VdAvgHisto.Fill(RB_MOD_LIST[i][2])
   if float(RB_MOD_LIST[i][2]) < 2.8:
      print 'Vd Outlier Module ' + str(i) + ' ' + RB_MOD_LIST[i][0] + '   Vd = ' + str(RB_MOD_LIST[i][2])
   VaAvgHisto.Fill(RB_MOD_LIST[i][3])
   if float(RB_MOD_LIST[i][3]) < 1.85:
      print 'Va Outlier Module ' + str(i) + ' ' + RB_MOD_LIST[i][0] + '   Va = ' + str(RB_MOD_LIST[i][3])

HCs = ['BmI','BmO','BpI','BpO']
Ds = ['1','2','3']
BLDsRNG1 = ['1','2','3','4','5','6','7','8','9','10','11']
BLDsRNG2 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','15','16','17']
PNLs = ['1','2']
RNGs = ['1','2']

VdHistoBLD_SumRNG1 = TH1F("VdHisto_RNG1", "Vd Histogram RNG1 Average over HCs, Disks, and Panels", 11 ,1 ,12)
VdHistoBLD_SumRNG1.GetXaxis().SetTitle("Blade")
VdHistoBLD_SumRNG1.GetYaxis().SetTitle("[V]")
VaHistoBLD_SumRNG1 = TH1F("VaHisto_RNG1", "Va Histogram RNG1 Average over HCs, Disks, and Panels", 11 ,1 ,12)
VaHistoBLD_SumRNG1.GetXaxis().SetTitle("Blade")
VaHistoBLD_SumRNG1.GetYaxis().SetTitle("[V]")
VdHistoBLD_SumRNG2 = TH1F("VdHisto_RNG2", "Vd Histogram RNG2 Average over HCs, Disks, and Panels", 17 ,1 ,18)
VdHistoBLD_SumRNG2.GetXaxis().SetTitle("Blade")
VdHistoBLD_SumRNG2.GetYaxis().SetTitle("[V]")
VaHistoBLD_SumRNG2 = TH1F("VaHisto_RNG2", "Va Histogram RNG2 Average over HCs, Disks, and Panels", 17 ,1 ,18)
VaHistoBLD_SumRNG2.GetXaxis().SetTitle("Blade")
VaHistoBLD_SumRNG2.GetYaxis().SetTitle("[V]")
VdHistoBLD_SumRNG1_DEN = TH1F("VdHisto_RNG1_DEN", "", 11 ,1 ,12)
VaHistoBLD_SumRNG1_DEN = TH1F("VaHisto_RNG1_DEN", "", 11 ,1 ,12)
VdHistoBLD_SumRNG2_DEN = TH1F("VdHisto_RNG2_DEN", "", 17 ,1 ,18)
VaHistoBLD_SumRNG2_DEN = TH1F("VaHisto_RNG2_DEN", "", 17 ,1 ,18)

for HC in HCs:
    VdHistoBLD_PNL_SumRNG1 = TH1F("VdHisto_"+str(HC)+"_RNG1", "Vd Histogram "+str(HC)+"_RNG1 Average over Disks and Panels", 11 ,1 ,12)
    VdHistoBLD_PNL_SumRNG1.GetXaxis().SetTitle("Blade")
    VdHistoBLD_PNL_SumRNG1.GetYaxis().SetTitle("[V]")
    VaHistoBLD_PNL_SumRNG1 = TH1F("VaHisto_"+str(HC)+"_RNG1", "Va Histogram "+str(HC)+"_RNG1 Average over Disks and Panels", 11 ,1 ,12)
    VaHistoBLD_PNL_SumRNG1.GetXaxis().SetTitle("Blade")
    VaHistoBLD_PNL_SumRNG1.GetYaxis().SetTitle("[V]")
    VdHistoBLD_PNL_SumRNG2 = TH1F("VdHisto_"+str(HC)+"_RNG2", "Vd Histogram "+str(HC)+"_RNG2 Average over Disks and Panels", 17 ,1 ,18)
    VdHistoBLD_PNL_SumRNG2.GetXaxis().SetTitle("Blade")
    VdHistoBLD_PNL_SumRNG2.GetYaxis().SetTitle("[V]")
    VaHistoBLD_PNL_SumRNG2 = TH1F("VaHisto_"+str(HC)+"_RNG2", "Va Histogram "+str(HC)+"_RNG2 Average over Disks and Panels", 17 ,1 ,18)
    VaHistoBLD_PNL_SumRNG2.GetXaxis().SetTitle("Blade")
    VaHistoBLD_PNL_SumRNG2.GetYaxis().SetTitle("[V]")
    VdHistoBLD_PNL_SumRNG1_DEN = TH1F("VdHisto_"+str(HC)+"_RNG1_DEN", "", 11 ,1 ,12)
    VaHistoBLD_PNL_SumRNG1_DEN = TH1F("VaHisto_"+str(HC)+"_RNG1_DEN", "", 11 ,1 ,12)
    VdHistoBLD_PNL_SumRNG2_DEN = TH1F("VdHisto_"+str(HC)+"_RNG2_DEN", "", 17 ,1 ,18)
    VaHistoBLD_PNL_SumRNG2_DEN = TH1F("VaHisto_"+str(HC)+"_RNG2_DEN", "", 17 ,1 ,18)
    for PNL in PNLs:
        VdHistoBLD_HC_SumRNG1 = TH1F("VdHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG1", "Vd Histogram "+str(HC)+"_PNL"+str(PNL)+"_RNG1 Average over Disks", 11 ,1 ,12)
        VdHistoBLD_HC_SumRNG1.GetXaxis().SetTitle("Blade")
        VdHistoBLD_HC_SumRNG1.GetYaxis().SetTitle("[V]")
        VaHistoBLD_HC_SumRNG1 = TH1F("VaHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG1", "Va Histogram "+str(HC)+"_PNL"+str(PNL)+"_RNG1 Average over Disks", 11 ,1 ,12)
        VaHistoBLD_HC_SumRNG1.GetXaxis().SetTitle("Blade")
        VaHistoBLD_HC_SumRNG1.GetYaxis().SetTitle("[V]")
        VdHistoBLD_HC_SumRNG2 = TH1F("VdHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG2", "Vd Histogram "+str(HC)+"_PNL"+str(PNL)+"_RNG2 Average over Disks", 17 ,1 ,18)
        VdHistoBLD_HC_SumRNG2.GetXaxis().SetTitle("Blade")
        VdHistoBLD_HC_SumRNG2.GetYaxis().SetTitle("[V]")
        VaHistoBLD_HC_SumRNG2 = TH1F("VaHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG2", "Va Histogram "+str(HC)+"_PNL"+str(PNL)+"_RNG2 Average over Disks", 17 ,1 ,18)
        VaHistoBLD_HC_SumRNG2.GetXaxis().SetTitle("Blade")
        VaHistoBLD_HC_SumRNG2.GetYaxis().SetTitle("[V]")
        VdHistoBLD_HC_SumRNG1_DEN = TH1F("VdHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG1", "", 11 ,1 ,12)
        VaHistoBLD_HC_SumRNG1_DEN = TH1F("VaHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG1", "", 11 ,1 ,12)
        VdHistoBLD_HC_SumRNG2_DEN = TH1F("VdHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG2", "", 17 ,1 ,18)
        VaHistoBLD_HC_SumRNG2_DEN = TH1F("VaHisto_"+str(HC)+"_PNL"+str(PNL)+"_RNG2", "", 17 ,1 ,18)
        for D in Ds:
            for RNG in RNGs:
                if RNG == '1':
                    VdHistoBLD = TH1F("VdHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1", "Vd Histogram "+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1", 11 ,1 ,12)
                    VaHistoBLD = TH1F("VaHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1", "Va Histogram "+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1", 11 ,1 ,12)
                    VdHistoBLD.GetYaxis().SetRangeUser(2.75,3.25)
                    VaHistoBLD.GetYaxis().SetRangeUser(1.75,2.25)
                    for BLD in BLDsRNG1:
                        for i in range(1,len(RB_MOD_LIST)):
                            if RB_MOD_LIST[i][0] == 'FPix_'+str(HC)+'_D'+str(D)+'_BLD'+str(BLD)+'_PNL'+str(PNL)+'_RNG1':
                                VdHistoBLD.SetBinContent(int(BLD),RB_MOD_LIST[i][2])
                                VaHistoBLD.SetBinContent(int(BLD),RB_MOD_LIST[i][3])
                    for i in range(1,12):
                        if VdHistoBLD.GetBinContent(i) > 0.0:
                            VdHistoBLD_PNL_SumRNG1_DEN.AddBinContent(i,1.)
                            VdHistoBLD_HC_SumRNG1_DEN.AddBinContent(i,1.)
                            VdHistoBLD_SumRNG1_DEN.AddBinContent(i,1.)
                        
                        if VaHistoBLD.GetBinContent(i) > 0.0:
                            VaHistoBLD_PNL_SumRNG1_DEN.AddBinContent(i,1.)
                            VaHistoBLD_HC_SumRNG1_DEN.AddBinContent(i,1.)
                            VaHistoBLD_SumRNG1_DEN.AddBinContent(i,1.)
                    
                    VdHistoBLD_PNL_SumRNG1.Add(VdHistoBLD)
                    VaHistoBLD_PNL_SumRNG1.Add(VaHistoBLD)
                    VdHistoBLD_HC_SumRNG1.Add(VdHistoBLD)
                    VaHistoBLD_HC_SumRNG1.Add(VaHistoBLD)
                    VdHistoBLD_SumRNG1.Add(VdHistoBLD)
                    VaHistoBLD_SumRNG1.Add(VaHistoBLD)
                    p.cd()
                    #VdHistoBLD.Write("VdHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1")
                    #VaHistoBLD.Write("VaHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG1")
                    VdHistoBLD.Reset()
                    VaHistoBLD.Reset()
                elif RNG == '2':
                    VdHistoBLD = TH1F("VdHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2", "Vd Histogram "+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2", 17 ,1 ,18)
                    VaHistoBLD = TH1F("VaHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2", "Va Histogram "+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2", 17 ,1 ,18)
                    VdHistoBLD.GetYaxis().SetRangeUser(2.75,3.25)
                    VaHistoBLD.GetYaxis().SetRangeUser(1.75,2.25)
                    for BLD in BLDsRNG2:
                        for i in range(1,len(RB_MOD_LIST)):
                            if RB_MOD_LIST[i][0] == 'FPix_'+str(HC)+'_D'+str(D)+'_BLD'+str(BLD)+'_PNL'+str(PNL)+'_RNG2':
                                VdHistoBLD.SetBinContent(int(BLD),RB_MOD_LIST[i][2])
                                VaHistoBLD.SetBinContent(int(BLD),RB_MOD_LIST[i][3])
                    for i in range(1,18):
                        if VdHistoBLD.GetBinContent(i) > 0.0:
                            VdHistoBLD_PNL_SumRNG2_DEN.AddBinContent(i,1.)
                            VdHistoBLD_HC_SumRNG2_DEN.AddBinContent(i,1.)
                            VdHistoBLD_SumRNG2_DEN.AddBinContent(i,1.)
                        
                        if VaHistoBLD.GetBinContent(i) > 0.0:
                            VaHistoBLD_PNL_SumRNG2_DEN.AddBinContent(i,1.)
                            VaHistoBLD_HC_SumRNG2_DEN.AddBinContent(i,1.)
                            VaHistoBLD_SumRNG2_DEN.AddBinContent(i,1.)
                    
                    VdHistoBLD_PNL_SumRNG2.Add(VdHistoBLD)
                    VaHistoBLD_PNL_SumRNG2.Add(VaHistoBLD)
                    VdHistoBLD_HC_SumRNG2.Add(VdHistoBLD)
                    VaHistoBLD_HC_SumRNG2.Add(VaHistoBLD)
                    VdHistoBLD_SumRNG2.Add(VdHistoBLD)
                    VaHistoBLD_SumRNG2.Add(VaHistoBLD)

                    p.cd()
                    #VdHistoBLD.Write("VdHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2")
                    #VaHistoBLD.Write("VaHisto_"+str(HC)+"_D"+str(D)+"_PNL"+str(PNL)+"_RNG2")
                    VdHistoBLD.Reset()
                    VaHistoBLD.Reset()
        VdHistoBLD_HC_SumRNG1.Divide(VdHistoBLD_HC_SumRNG1_DEN)
        VaHistoBLD_HC_SumRNG1.Divide(VaHistoBLD_HC_SumRNG1_DEN)
        VdHistoBLD_HC_SumRNG2.Divide(VdHistoBLD_HC_SumRNG2_DEN)
        VaHistoBLD_HC_SumRNG2.Divide(VaHistoBLD_HC_SumRNG2_DEN)
        p.cd()
        VdHistoBLD_HC_SumRNG1.Write("Vd_"+str(HC)+"_PNL"+str(PNL)+"_RNG1_Average")
        VdHistoBLD_HC_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
        VdHistoBLD_HC_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
        VaHistoBLD_HC_SumRNG1.Write("Va_"+str(HC)+"_PNL"+str(PNL)+"_RNG1_Average")
        VaHistoBLD_HC_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
        VaHistoBLD_HC_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
        VdHistoBLD_HC_SumRNG2.Write("Vd_"+str(HC)+"_PNL"+str(PNL)+"_RNG2_Average")
        VdHistoBLD_HC_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
        VdHistoBLD_HC_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
        VaHistoBLD_HC_SumRNG2.Write("Va_"+str(HC)+"_PNL"+str(PNL)+"_RNG2_Average")
        VaHistoBLD_HC_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
        VaHistoBLD_HC_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
        VdHistoBLD_HC_SumRNG1.Reset()
        VaHistoBLD_HC_SumRNG1.Reset()
        VdHistoBLD_HC_SumRNG2.Reset()
        VaHistoBLD_HC_SumRNG2.Reset()
    VdHistoBLD_PNL_SumRNG1.Divide(VdHistoBLD_PNL_SumRNG1_DEN)
    VaHistoBLD_PNL_SumRNG1.Divide(VaHistoBLD_PNL_SumRNG1_DEN)
    VdHistoBLD_PNL_SumRNG2.Divide(VdHistoBLD_PNL_SumRNG2_DEN)
    VaHistoBLD_PNL_SumRNG2.Divide(VaHistoBLD_PNL_SumRNG2_DEN)
    p.cd()
    VdHistoBLD_PNL_SumRNG1.Write("Vd_"+str(HC)+"_RNG1_Average")
    VdHistoBLD_PNL_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
    VdHistoBLD_PNL_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
    VaHistoBLD_PNL_SumRNG1.Write("Va_"+str(HC)+"_RNG1_Average")
    VaHistoBLD_PNL_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
    VaHistoBLD_PNL_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
    VdHistoBLD_PNL_SumRNG2.Write("Vd_"+str(HC)+"_RNG2_Average")
    VdHistoBLD_PNL_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
    VdHistoBLD_PNL_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
    VaHistoBLD_PNL_SumRNG2.Write("Va_"+str(HC)+"_RNG2_Average")
    VaHistoBLD_PNL_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
    VaHistoBLD_PNL_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
    VdHistoBLD_PNL_SumRNG1.Reset()
    VaHistoBLD_PNL_SumRNG1.Reset()
    VdHistoBLD_PNL_SumRNG2.Reset()
    VaHistoBLD_PNL_SumRNG2.Reset()
VdHistoBLD_SumRNG1.Divide(VdHistoBLD_SumRNG1_DEN)
VaHistoBLD_SumRNG1.Divide(VaHistoBLD_SumRNG1_DEN)
VdHistoBLD_SumRNG2.Divide(VdHistoBLD_SumRNG2_DEN)
VaHistoBLD_SumRNG2.Divide(VaHistoBLD_SumRNG2_DEN)



p.cd()
VdHistoBLD_SumRNG1.Write("Vd_RNG1_Average")
VdHistoBLD_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
VdHistoBLD_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
VaHistoBLD_SumRNG1.Write("Va_RNG1_Average")
VaHistoBLD_SumRNG1.GetYaxis().SetRangeUser(2.75,3.25)
VaHistoBLD_SumRNG1.GetYaxis().SetRangeUser(1.75,2.25)
VdHistoBLD_SumRNG2.Write("Vd_RNG2_Average")
VdHistoBLD_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
VdHistoBLD_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
VaHistoBLD_SumRNG2.Write("Va_RNG2_Average")
VaHistoBLD_SumRNG2.GetYaxis().SetRangeUser(2.75,3.25)
VaHistoBLD_SumRNG2.GetYaxis().SetRangeUser(1.75,2.25)
VdHisto.Write("Vd")
VaHisto.Write("Va")
VdAvgHisto.Write("VdAvg")
VaAvgHisto.Write("VaAvg")
VdPlot.Write("VdPlot")
VaPlot.Write("VaPlot")
p.Close()



