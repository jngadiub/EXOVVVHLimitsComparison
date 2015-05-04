import ROOT
from array import array
from ROOT import *
import sys
import time

fname = 'EXOVH_ALL_UL_HybridNew.root'
infile = ROOT.TFile.Open(fname,"READ")

c = ROOT.TCanvas()
infile.GetObject("c_lim_HybridNew",c)
 
obj = ROOT.TObject()
next = ROOT.TIter(c.GetListOfPrimitives())
obj = next()
g=0
while obj:
   g+=1
   print "#############################"
   print g,obj.GetName()
   if obj and obj.InheritsFrom("TGraph"): #and g > 2:
      gr = ROOT.TGraph(obj)
      x = ROOT.Double(0.)
      y = ROOT.Double(0.)
      for p in xrange(0,gr.GetN()):
        gr.GetPoint(p,x,y)
	if g == 7:
	   print "%.1f obs %.6f" %(x,y)
   obj = next()   

infile.Close()
infile.Delete()
