import ROOT
from array import array
from ROOT import *

fname = 'brazilianFlag_WZ_combined.root'
infile = ROOT.TFile.Open(fname,"READ")

c = ROOT.TCanvas()
infile.GetObject("c1",c)

obs = array('d',[])
exp = array('d',[])
sigma1 = array('d',[])
sigma2 = array('d',[])
m = array('d',[])
m_sigma = array('d',[])

reduce = 1.

obj = ROOT.TObject()
next = ROOT.TIter(c.GetListOfPrimitives())
obj = next()
g=0
while obj:
   g+=1
   if obj and obj.InheritsFrom("TGraph") and g > 2:
      gr = ROOT.TGraph(obj)
      x = ROOT.Double(0.)
      y = ROOT.Double(0.)
      for p in xrange(0,gr.GetN()):
        gr.GetPoint(p,x,y)
	if g == 3:
	   sigma2.append(y/reduce)
	   m_sigma.append(x)
	elif g == 4:
	   sigma1.append(y/reduce)   
	if g == 5:
	   exp.append(y/reduce)
	   m.append(x)
	elif g == 6:
	   obs.append(y/reduce)
   obj = next()   

infile.Close()
infile.Delete()

outfile = ROOT.TFile("Limits_EXO_12_024.root","RECREATE")

npoints = len(m)

gr_exp = ROOT.TGraph(npoints,m,exp)
gr_obs = ROOT.TGraph(npoints,m,obs)

npoints = len(m_sigma)
gr_sigma1 = ROOT.TGraph(npoints,m_sigma,sigma1)
gr_sigma2 = ROOT.TGraph(npoints,m_sigma,sigma2)

gr_exp.SetName("EXPECTED")
gr_obs.SetName("OBSERVED")
gr_sigma1.SetName("ONESIGMA")
gr_sigma2.SetName("TWOSIGMA")

gr_exp.Write()
gr_obs.Write()
gr_sigma1.Write()
gr_sigma2.Write()

outfile.Write()
outfile.Close()
