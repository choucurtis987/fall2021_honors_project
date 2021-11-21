import matplotlib as mpl
mpl.rc('figure',facecolor='white')
mpl.rc('lines', markersize = 1.6 )
mpl.rc('lines', markeredgewidth = 0.0 )
mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
import matplotlib.pyplot as plt
import time
import matplotlib.dates as dt
import numpy as np
import datetime
import ROOT

wavfit = ROOT.TF1('wavfit','0.5*[0]*TMath::Erfc((10.0-x)/[4])*TMath::Exp((x-10.0)/-[3]) - 0.5*[1]*TMath::Erfc((81.9-x)/[5])*TMath::Exp((x-10.0)/-[3])+[2]')


wfmpre = '1;8;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";8.0E-4;0.0E0;-5.4E1;"V"'

t = [ 1.0e6*(float(wfmpre.split(';')[8])*float(i)+float(wfmpre.split(';')[10])) for i in range(0,500) ]

wavfit.SetParameter(0,46.685)
wavfit.SetParameter(1,46.405)
wavfit.SetParameter(2,40.235)
wavfit.FixParameter(3,395.3)
wavfit.FixParameter(4,1.0)
wavfit.FixParameter(5,2.9)

with open('raw_sig.dat') as ff:
    for line in ff:
        try :
            wfm = [ float(u) for u in line.split(',') ]
        except ValueError:
            continue
with open('raw_bkg.dat') as ff:
    for line in ff:
        try :
            raw_bkg = [ float(u) for u in line.split(',') ]
        except ValueError:
            continue

volt = [ 1.0e3*(( dl - float(wfmpre.split(';')[14]) )*float(wfmpre.split(';')[12]) - float(wfmpre.split(';')[13])) for dl in wfm ]
bkg = [ 1.0e3*(( dl - float(wfmpre.split(';')[14]) )*float(wfmpre.split(';')[12]) - float(wfmpre.split(';')[13])) for dl in raw_bkg ]

volt = [ v[0] - v[1] for v in zip( volt , bkg ) ]
wg = ROOT.TGraph()

[ wg.SetPoint(wg.GetN(),v[0],v[1]) for v in zip(t,volt) ]

wg.Draw('alp')
ROOT.gStyle.SetOptFit(111111)
wg.Fit(wavfit)

