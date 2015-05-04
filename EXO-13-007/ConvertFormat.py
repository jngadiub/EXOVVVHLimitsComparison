import ROOT
from array import array
from ROOT import *

fname = 'LimitAllChannel.root'
infile = ROOT.TFile.Open(fname,"READ")

brhtt = 0.0637
brzqq = 0.6991

#reduce = 1.
reduce = brhtt*brzqq

obs = array('d',[])
exp = array('d',[])
sigma1 = array('d',[])
sigma2 = array('d',[])
m = array('d',[])
m_sigma = array('d',[])

x = ROOT.Double(0.)
y = ROOT.Double(0.)

gr = ROOT.TGraph(infile.Get("OBSERVED"))
npoints = gr.GetN()
for p in xrange(0,npoints):
   gr.GetPoint(p,x,y)
   obs.append(y/(reduce*1000.))
   m.append(x/1000.) 

gr = ROOT.TGraph(infile.Get("EXPECTED"))
npoints = gr.GetN()
for p in xrange(0,npoints):
   gr.GetPoint(p,x,y)
   exp.append(y/(reduce*1000.))

gr = ROOT.TGraph(infile.Get("OneSigma"))
npoints = gr.GetN()
for p in xrange(0,npoints):
   gr.GetPoint(p,x,y)
   sigma1.append(y/(reduce*1000.))
   m_sigma.append(x/1000.)

gr = ROOT.TGraph(infile.Get("TwoSigma"))
npoints = gr.GetN()
for p in xrange(0,npoints):
   gr.GetPoint(p,x,y)
   sigma2.append(y/(reduce*1000.))

outfile = ROOT.TFile("Limits_EXO_13_007.root","RECREATE")

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
      
gr_exp.Write()
gr_obs.Write()
gr_sigma1.Write()
gr_sigma2.Write()

outfile.Write()
outfile.Close()
   
infile.Close()
infile.Delete()
