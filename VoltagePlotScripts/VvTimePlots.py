#!/user/local/bin/python                                                                                                                                                                                                                                                                        
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

# Luminosities for each measurment 0, 6.3, 18.1, 24.2, 49.48

gStyle.SetOptStat(0)

RNGs = ["1","2"]
ADs = ["Vd","Va","Vdr","Var","Vbg","VbgCor","dose","VdCor","VaCor","VdrCor","VarCor","VbgFullCor","CorVdr","CorVar","CorVbg"]

CorAD = ["VdCor","VaCor","VdrCor","VarCor","VbgFullCor"]

M_plots = TFile("plots_May.root", "read")
J_plots = TFile("plots_Jul.root", "read")
A_plots = TFile("plots_Aug.root", "read")
S_plots = TFile("plots_Sept.root", "read")
D_plots = TFile("plots_Dec.root", "read")

dict = {}
dict['Vd'] = [2.9,3.1]
dict['Va'] = [1.9,2.1]
dict['Vdr'] = [170,190]
dict['Var'] = [110,125]
dict['Vbg'] = [140,155]
dict['VbgCor'] = [135,155]
dict['dose'] = [-0.05,0.075]
dict['VdCor'] = [2.9,3.1]
dict['VaCor'] = [1.9,2.1]
dict['VdrCor'] = [170,190]
dict['VarCor'] = [110,125]
dict['VbgFullCor'] = [135,155]
dict['CorVdr'] = [.85,1.15]
dict['CorVar'] = [.85,1.15]
dict['CorVbg'] = [.85,1.15]

dictY = {}
dictY['Vd'] = "V"
dictY['Va'] = "V"
dictY['Vdr'] = "V"
dictY['Var'] = "V"
dictY['Vbg'] = "V"
dictY['VbgCor'] = "V"
dictY['dose'] = "MGy"
dictY['VdCor'] = "V"
dictY['VaCor'] = "V"
dictY['VdrCor'] = "V"
dictY['VarCor'] = "V"
dictY['VbgFullCor'] = "V"
dictY['CorVdr'] = "Correction"
dictY['CorVar'] = "Correction"
dictY['CorVbg'] = "Correction"

for RNG in RNGs:
    totDev = 0.0
    d = 0.0
    for AD in ADs:
        canvas = TCanvas()
        canvas.Clear()
        canvas.Divide(1, 1)

        inputHisto_M = M_plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
        inputHisto_M.SetMaximum(dict[AD][1])
        inputHisto_M.SetMinimum(dict[AD][0])
        inputHisto_M.SetLineColor(2)
        inputHisto_M.SetLineWidth(2)
        inputHisto_M.GetXaxis().SetTitle("ROC Group")
        inputHisto_M.GetYaxis().SetTitle(dictY[AD])
        inputHisto_J = J_plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
        inputHisto_J.SetLineColor(3)
        inputHisto_J.SetLineWidth(2)
        inputHisto_A = A_plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
        inputHisto_A.SetLineColor(6)
        inputHisto_A.SetLineWidth(2)
        inputHisto_S = S_plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
        inputHisto_S.SetLineColor(7)
        inputHisto_S.SetLineWidth(2)
        inputHisto_D = D_plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
        inputHisto_D.SetLineColor(8)
        inputHisto_D.SetLineWidth(2)

        canvas.cd(1)
        canvas.SetGrid()
        gStyle.SetGridStyle(0)
        inputHisto_M.Draw("histsames")
        inputHisto_J.Draw("histsames")
        inputHisto_A.Draw("histsames")
        inputHisto_S.Draw("histsames")
        inputHisto_D.Draw("histsames")
        inputHisto_S.GetXaxis().SetAxisColor(17);
        inputHisto_S.GetYaxis().SetAxisColor(17);
        canvas.RedrawAxis()
        canvas.Update()

        leg = TLegend(.15,.2,.4,.4)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.035)
        leg.AddEntry(inputHisto_M,"L =  0.0 1/fb","L")
        leg.AddEntry(inputHisto_J,"L =  6.3 1/fb","L")
        leg.AddEntry(inputHisto_A,"L = 18.1 1/fb","L")
        leg.AddEntry(inputHisto_S,"L = 24.2 1/fb","L")
        leg.AddEntry(inputHisto_D,"L = 49.98 1/fb","L")
        leg.Draw()

        canvas.Update()
        canvas.SaveAs("IMG/plotImg_"+AD+"RNG"+RNG+".pdf")

        if AD in CorAD:
            #print "Value: " + AD
            avg = 0.0
            c = 0.0
            for i in range (1,9):
                avg += float(inputHisto_D.GetBinContent(i))
                c += 1.0
            avg = avg/c
            #print "    AVG: " + str(avg)
            avgDev = 0.0
            for i in range (1,9):
                diff = abs(float(inputHisto_D.GetBinContent(i)) - avg)/avg
                avgDev += diff
            avgDev = avgDev/c
            #print "AVG Dev: " + str(avgDev)
            totDev += avgDev
            d += 1.

        #for i in range (1,9):
            #print 'Position ' + str(i-1) + '  Value: ' + str(float(inputHisto_S.GetBinContent(i)))
        #for i in range (1,9):
            #print 'Position ' + str(i-1) + '  Factor: ' + str(float(inputHisto_S.GetBinContent(i))/float(inputHisto_S.GetBinContent(1)))

    totDev = totDev/d
    print "RNG " +  str(RNG) + " Total Dev: " + str(totDev)



