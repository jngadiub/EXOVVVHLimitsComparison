import ROOT
from array import array
from ROOT import *
import sys
import time
        
obs = array('d',[])
exp = array('d',[])
sigma1 = array('d',[])
sigma2 = array('d',[])
m = array('d',[])
m_sigma = array('d',[])

fname = 'WprimeWZTo3LNu_LimitVMass.root'
f = ROOT.TFile(fname)
t = f.Get("")
nentries = t.GetEntries()

#br = 0.108*0.033658
br = 0.2132*0.06729
 
for e in xrange(0,nentries):
   t.GetEntry(e)
   if t.Mass < 800:
      continue   
   m.append(t.Mass/1000)
   m_sigma.append(t.Mass/1000)
   obs.append(t.ObsLimit/br)
   exp.append(t.ExpLimit/br)
   sigma1.append(t.ExpLimitM1/br)
   sigma2.append(t.ExpLimitM2/br)
   print "mass %.1f exp %.5f obs %.5f/%.5f" %(t.Mass/1000,t.ExpLimit/br,t.ObsLimit/br,t.ObsLimit)

e = nentries-1
while e >= 0 and t.Mass > 800:
   t.GetEntry(e)
   e = e-1
   m_sigma.append(t.Mass/1000)
   sigma1.append(t.ExpLimitP1/br)
   sigma2.append(t.ExpLimitP2/br)

outfile = ROOT.TFile("Limits_EXO_12_025.root","RECREATE")

npoints = len(m)   
gr_obs = ROOT.TGraph(npoints,m,obs)
gr_obs.SetName("OBSERVED")

gr_exp = ROOT.TGraph(npoints,m,exp)
gr_exp.SetName("EXPECTED")

npoints = len(m_sigma)
gr_sigma1 = ROOT.TGraph(npoints,m_sigma,sigma1)
gr_sigma1.SetName("ONESIGMA")

gr_sigma2 = ROOT.TGraph(npoints,m_sigma,sigma2)
gr_sigma2.SetName("TWOSIGMA")

gr_obs.Draw("ALP")
gr_exp.Draw("Lsame")

time.sleep(1000)
      
gr_exp.Write()
gr_obs.Write()
gr_sigma1.Write()
gr_sigma2.Write()
