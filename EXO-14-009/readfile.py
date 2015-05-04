import ROOT
from array import array
from ROOT import *
import sys
import time

fname = 'EXOVH_xvh_UL_Asymptotic.root'
infile = ROOT.TFile.Open(fname,"READ")

c = ROOT.TCanvas()
infile.GetObject("c_lim_Asymptotic",c)

obs = array('d',[])
exp = array('d',[])
sigma1 = array('d',[])
sigma2 = array('d',[])
m = array('d',[])
m_sigma = array('d',[])
  
obj = ROOT.TObject()
next = ROOT.TIter(c.GetListOfPrimitives())
obj = next()
g=0
while obj:
   g+=1
   print "#############################"
   print g,obj.GetName()
   if obj and obj.InheritsFrom("TGraph"): #and g > 2:
      print g,obj.GetName()
      gr = ROOT.TGraph(obj)
      x = ROOT.Double(0.)
      y = ROOT.Double(0.)
      for p in xrange(0,gr.GetN()):
        gr.GetPoint(p,x,y)
	if g == 7:
	   print "%.1f obs %.6f" %(x,y)
	   obs.append(y)
	   m.append(x/1000)
	if g == 6:
	   #print "%.1f exp %.6f" %(x,y)
	   exp.append(y)
	if g==4:
	   sigma1.append(y)
	   m_sigma.append(x/1000)
	if g==3:
	   sigma2.append(y)	         
   obj = next()   

infile.Close()
infile.Delete()

outfile = ROOT.TFile("Limits_EXO_14_009_HV.root","RECREATE")

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
