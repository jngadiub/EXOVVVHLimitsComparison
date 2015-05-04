import ROOT
from array import array
from ROOT import *
import sys

def getAsymLimits(file):
    
    
    f = ROOT.TFile(file);
    t = f.Get("limit");
    entries = t.GetEntries();
    
    lims = [0,0,0,0,0,0];
    
    for i in range(entries):
        
        t.GetEntry(i);
        t_quantileExpected = t.quantileExpected;
        t_limit = t.limit;
        
        #print "limit: ", t_limit, ", quantileExpected: ",t_quantileExpected;
        
        if t_quantileExpected == -1.: lims[0] = t_limit;
        elif t_quantileExpected >= 0.024 and t_quantileExpected <= 0.026: lims[1] = t_limit;
        elif t_quantileExpected >= 0.15  and t_quantileExpected <= 0.17:  lims[2] = t_limit;
        elif t_quantileExpected == 0.5: lims[3] = t_limit;
        elif t_quantileExpected >= 0.83  and t_quantileExpected <= 0.85:  lims[4] = t_limit;
        elif t_quantileExpected >= 0.974 and t_quantileExpected <= 0.976: lims[5] = t_limit;
        else: print "Unknown quantile!"
    
    return lims;
        

brWqq = 0.6991
brZqq = 0.676

channels = ['HW','HZ','HV']
dirs = ['HVCombinedLimits','HVCombinedLimits','HVCombinedLimits']
#brs = [brWqq/0.01,brZqq/0.01,brWqq*brZqq/0.01]
brs = [brWqq/0.01,brZqq/0.01,(brWqq+brZqq)/0.03]

for c in xrange(0,len(channels)):

 print "***************** "
 print channels[c],dirs[c]
 print "***************** "
 
 mlow = 1000.
 mhigh = 2600.
 npoints = int((mhigh-mlow)/100)

 obs = array('d',[])
 exp = array('d',[])
 sigma1 = array('d',[])
 sigma2 = array('d',[])
 m = array('d',[])
 m_sigma = array('d',[])

 for p in xrange(0,npoints+1):
   mass = mlow+p*100
   fname = '%s/higgsCombine%sqq.Asymptotic.mH%0.f.root' %(dirs[c],channels[c],mass)
   m.append(mass/1000)
   m_sigma.append(mass/1000)
   limits = getAsymLimits(fname)
   obs.append(limits[0]/brs[c])   
   exp.append(limits[3]/brs[c])
   sigma1.append(limits[2]/brs[c])
   sigma2.append(limits[1]/brs[c])
   #print "mass %.1f observed limit %f expected %f" %(mass/1000,limits[0]/brs[c],limits[3]/brs[c])

 for p in xrange(0,npoints+1):
   mass = mhigh-p*100
   fname = '%s/higgsCombine%sqq.Asymptotic.mH%0.f.root' %(dirs[c],channels[c],mass)
   limits = getAsymLimits(fname)
   m_sigma.append(mass/1000)
   sigma1.append(limits[4]/brs[c])
   sigma2.append(limits[5]/brs[c])
   #print "mass %.1f sigma 1 %f" %(mass/1000,limits[4]/br)
   
   outfile = ROOT.TFile("Limits_EXO_14_009_%s.root" %(channels[c]),"RECREATE")

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
