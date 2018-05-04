#!/user/local/bin/python                                                                                                                                                      
from decimal import Decimal
import subprocess
import os
import sys
import math
import numpy as np
from ROOT import *

gStyle.SetOptStat(0)

inFilePvD = open("PercShiftVbg_Dose_V2.csv","read")

points = []
for line in inFilePvD:
    points.append([float(line.split(',')[0]),float(line.split(',')[1])])
print points

X = np.zeros(len(points))
Y = np.zeros(len(points))    
for i in range(0,len(points)):
    X[i] = points[i][0]
    Y[i] = points[i][1]
tempGraph = TGraph(len(points),X,Y)
tempGraph.Draw()


#myFit = TF1("myFit","(13.5/(1+ TMath::Exp(-[1]*(x-[2]))))",0.,5.)
myFit = TF1("myFit","([0]*x/(1+[1]*x))",0.,5.)         
tempGraph.Fit("myFit")

outFileFit = TFile("PercShiftVbg_Dose.root","recreate")

outFileFit.cd()
myFit.Write("ErfFit")
tempGraph.Write("points")
outFileFit.Close()
