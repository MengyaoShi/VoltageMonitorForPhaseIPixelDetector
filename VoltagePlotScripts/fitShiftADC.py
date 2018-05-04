#!/user/local/bin/python                                                                                                                                                      
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

gStyle.SetOptStat(0)

lumINDEX = {'May': 0.0, 'Jul': 6.3, 'Aug': 18.1, 'Sept': 24.2, 'Dec': 49.98}
MEAS = ['May','Jul','Aug','Sept','Dec']
RNGs = ['1','2']
ADs = ['VbgCor']
BaseINDEX = {'1':148.202,'2':148.433}

for RNG in RNGs:
    outFileFit = TFile("ShiftR"+RNG+"ADC.root","recreate")
    points = []
    for AD in ADs:
        for M in MEAS:
            plots = TFile("plots_"+M+".root", "read")
            inputHistoVbg = plots.Get(AD+"CombROC_RNG"+RNG+"_Average")
            inputHistoDose = plots.Get("doseCombROC_RNG"+RNG+"_Average")
            for i in range (1,inputHistoVbg.GetXaxis().GetNbins()+1):
                points.append([inputHistoDose.GetBinContent(i),inputHistoVbg.GetBinContent(i)/BaseINDEX[RNG]])
                #print "Meas: " + str(M) + "   " + str([inputHistoDose.GetBinContent(i),inputHistoVbg.GetBinContent(i)])

    points.sort()

    #print str(points)

    X = np.zeros(len(points))
    Y = np.zeros(len(points))    
    for i in range(0,len(points)):
        X[i] = points[i][0]
        Y[i] = points[i][1]
    tempGraph = TGraph(len(points),X,Y)
    tempGraph.Draw()

    #myFit = TF1("myFit","(13.5/(1+ TMath::Exp(-[1]*(x-[2]))))",0.,5.)
    #myFit = TF1("myFit","[1]*(1-(log(1+[0]*x)))",0.,0.1)
    #myFit = TF1("myFit","[0]*x+[1]",0.,0.1)
    #myFit = TF1("myFit","1-TMath::Erf([0]*x)",0.,0.1)
    myFit = TF1("myFit","[0]*(1.0-TMath::Erf([1]*x))+[2]",0.,1.5)
    tempGraph.Fit("myFit")

    outFileFit.cd()
    myFit.Write("LnFit")
    tempGraph.Write("points")

    outFileFit.Close()
