import ROOT
import time
from array import array
from ROOT import *
import CMS_lumi, tdrstyle
import sys,os
from optparse import OptionParser

def get_canvas(cname):

  tdrstyle.setTDRStyle()
  CMS_lumi.lumi_8TeV = "19.7 fb^{-1}"
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Preliminary"

  iPos = 0
  if( iPos==0 ): CMS_lumi.relPosX = 0.16

  H_ref = 800; 
  W_ref = 800; 
  W = W_ref
  H  = H_ref

  T = 0.08*H_ref
  B = 0.12*H_ref 
  L = 0.12*W_ref
  R = 0.04*W_ref

  canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)
  canvas.SetLeftMargin( L/W+0.02 )
  canvas.SetRightMargin( R/W )
  canvas.SetTopMargin( T/H )
  canvas.SetBottomMargin( B/H )
  canvas.SetGrid()
  canvas.SetLogy()
  
  return canvas

def get_legend(model):

   legs = []
   if model.find('X0') != -1:
      legs.append( ROOT.TLegend(0.52,0.63,0.93,0.88) )
   elif model.find('Xpm') != -1:
      legs.append( ROOT.TLegend(0.52,0.53,0.93,0.88) )
   else:   
      legs.append( ROOT.TLegend(0.47,0.73,0.74,0.87) )
      legs.append( ROOT.TLegend(0.47,0.59,0.74,0.73) )

   for l in legs:      
      l.SetBorderSize(0)
      l.SetFillStyle(0)
      l.SetTextSize(0.02202073)
      l.SetTextFont(42)
   
   return legs

def get_legend_theo(model):

   if model != 'TripletX':
      l = ROOT.TLegend(0.26,0.17,0.54,0.28)
   else:
      l = ROOT.TLegend(0.76,0.20,0.95,0.24)
      
   l.SetBorderSize(0)
   l.SetFillStyle(0)
   l.SetTextSize(0.03)
   l.SetTextFont(42)
   
   return l

def get_theo_map():

   V0_mass = array('d',[])
   Vp_mass = array('d',[])

   brs = {}
   index = {}

   mapping = ["M0","M+","BRWW","BRhZ","BRZW","BRWh","CX+(pb)","CX0(pb)","CX-(pb)"]

   for m in xrange(0,len(mapping)):
      if mapping[m] != "M0" and mapping[m] != "M+":
   	 brs[mapping[m]] = array('d',[])
   	 #print mapping[m]

   f = open('HVTcrossSection.txt','r')
   for line in f:
      brDict = line.split(",")
      for d in xrange(0,len(brDict)):
   	 if brDict[d].find('\n') != -1:
   	    brDict[d] = brDict[d].split('\n')[0]
   	 for m in xrange(0,len(mapping)):
   	    if brDict[d] == mapping[m]:
   	       index[mapping[m]] = d
   	       #print "%s %i" %(mapping[m],d)
   	    
   f.close()

   f = open('HVTcrossSection.txt','r')

   l = 0
   for line in f:
      l+=1
      if l == 1:
   	 continue   
      brDict = line.split(",")  	    
      V0_mass.append(float(brDict[index['M0']])/1000)
      Vp_mass.append(float(brDict[index['M+']])/1000)
      for m in xrange(0,len(mapping)):
   	 if mapping[m] != "M0" and mapping[m] != "M+":
   	    brs[mapping[m]].append(float(brDict[index[mapping[m]]]))

   f.close()
   
   return [brs,V0_mass]
     
def convert_files():

   an = ['EXO-12-024','EXO-12-025','EXO-13-007','EXO-14-009','EXO-14-010','EXO-13-009']
   
   for i in xrange(0,len(an)):
      os.chdir(an[i])
      cmd = 'python ConvertFormat.py'
      os.system(cmd)
      os.chdir('../')
      cmd = 'mv %s/Limits_* .'%(an[i])
      os.system(cmd)
   
def get_map(model):

   flist = []
   palette = []
   leg = []
   sf = []
   d = {}  
   
   if model.find('Xpm') != -1:
      flist = ['EXO_12_025','EXO_14_010','EXO_13_007','EXO_14_009_HW','EXO_12_024','EXO_13_009_WW','EXO_13_009_ZZ']
      palette = [ROOT.TColor.kOrange+7,ROOT.TColor.kBlue,ROOT.kPink-1,ROOT.TColor.kAzure+10,210,ROOT.TColor.kPink+9,ROOT.TColor.kViolet+6]
      leg = ['X^{#pm} #rightarrow WZ #rightarrow 3l#nu (EXO-12-025)','X^{#pm} #rightarrow WH #rightarrow l#nuj (EXO-14-010)',
             'X^{#pm} #rightarrow WH #rightarrow j#tau#tau (EXO-13-007)','X^{#pm} #rightarrow WH #rightarrow jj (EXO-14-009)',
             'X^{#pm} #rightarrow WZ #rightarrow jj (EXO-12-024)','X^{#pm} #rightarrow WZ #rightarrow l#nuj (EXO-13-009)','X^{#pm} #rightarrow WZ #rightarrow jll (EXO-13-009)']
      lstyle = [1,1,1,1,1,1,1]
      if model.find('Singlet') != -1:	           
         sf = [1.,1.,1.,1.,1.,1.,1.]
      elif model.find('Triplet') != -1:
         sf = [1.,1.,1.5,1.5,1.5,1.5,1.] 
   elif model.find('X0') != -1:
      flist = ['EXO_13_007','EXO_14_009_HZ','EXO_12_024','EXO_13_009_WW']
      palette = [ROOT.kPink-1,ROOT.TColor.kAzure+10,210,ROOT.TColor.kBlue]
      leg = ['X^{0} #rightarrow ZH #rightarrow j#tau#tau (EXO-13-007)','X^{0} #rightarrow ZH #rightarrow jj (EXO-14-009)',
             'X^{0} #rightarrow WW #rightarrow jj (EXO-12-024)','X^{0} #rightarrow WW #rightarrow l#nuj (EXO-13-009)']
      lstyle = [1,1,1,1]
      if model.find('Singlet') != -1:
         sf = [1.,1.,1.,1.]      
      elif model.find('Triplet') != -1:
         sf = [3.,3.,3.,3.]       
   elif model == "TripletX":
      flist = ['EXO_12_025','EXO_12_024','EXO_13_009_WW','EXO_13_009_ZZ','EXO_14_010','EXO_13_007','EXO_14_009_HV']
      palette = [6,ROOT.TColor.kOrange-3,ROOT.TColor.kAzure+10,ROOT.TColor.kSpring-6,ROOT.TColor.kBlue,ROOT.TColor.kBlue,ROOT.TColor.kBlue]  
      leg = ['X #rightarrow WZ #rightarrow lll#nu (EXO-12-025)','X #rightarrow WV #rightarrow qqqq (EXO-12-024)',
             'X #rightarrow WV #rightarrow l#nuqq (EXO-13-009)','X #rightarrow WZ #rightarrow qqll (EXO-13-009)',
	     'X #rightarrow WH #rightarrow l#nubb (EXO-14-010)','X #rightarrow VH #rightarrow qq#tau#tau (EXO-13-007)',
	     'X #rightarrow VH #rightarrow qqbb,6q (EXO-14-009)']
      sf = [1.5,1.,1.,1.5,1.5,1.,1.]
      lstyle = [1,1,1,1,5,1,3]
      lsize = [3,3,3,3,3,2,3]
      
      
      
   d['flist'] = flist
   d['palette'] = palette
   d['leg'] = leg
   d['sf'] = sf
   d['lstyle'] = lstyle
   d['lsize'] = lsize
   
   return d

def get_theo_gr(model,brs_map,mass_map):

   v = array('d',[])
   newm = array('d',[])

   if model.find('Xpm') != -1:
      for m in xrange(0,len(mass_map)):
         v.append(brs_map['BRZW'][m]*(brs_map['CX+(pb)'][m]+brs_map['CX-(pb)'][m]))
   elif model.find('X0') != -1:
      for m in xrange(0,len(mass_map)):
         v.append(brs_map['BRWW'][m]*brs_map['CX0(pb)'][m])
   else:
      for m in xrange(0,len(mass_map)):
         if mass_map[m] > 0.8:
            v.append(brs_map['CX+(pb)'][m]+brs_map['CX-(pb)'][m]+brs_map['CX0(pb)'][m])
	    newm.append(mass_map[m])
	   #print m,mass_map[m],brs_map['CX+(pb)'][m]+brs_map['CX-(pb)'][m]+brs_map['CX0(pb)'][m] 

   #print "========================================="
   #print v[51]
   #print "========================================="

   gr_theo = ROOT.TGraph(len(newm),newm,v) 

   #x = ROOT.Double(0.)
   #y = ROOT.Double(0.)
   #for p in xrange(0,gr_theo.GetN()):
   #  gr_theo.GetPoint(p,x,y)
     #print x,y
        
   return gr_theo
         
def get_graph(fname,scale):

   print "### %s ###" %(fname)
   f = ROOT.TFile("Limits_%s.root"%(fname))
   grtmp_obs = f.Get("OBSERVED")
   grtmp_exp = f.Get("EXPECTED")
   
   m = array('d',[])
   y_obs = array('d',[])
   y_exp = array('d',[])
   npoints = grtmp_obs.GetN()  
   for p in xrange(0,npoints):
      g_x_obs = ROOT.Double(0.)
      g_y_obs = ROOT.Double(0.)
      grtmp_obs.GetPoint(p,g_x_obs,g_y_obs)
      m.append(g_x_obs)
      y_obs.append(g_y_obs*scale)
      g_x_exp = ROOT.Double(0.)
      g_y_exp = ROOT.Double(0.)
      grtmp_exp.GetPoint(p,g_x_exp,g_y_exp)
      y_exp.append(g_y_exp*scale)
      print "mass %.1f obs %f" %(g_x_obs,g_y_obs*scale) 
         
   f.Close()
   f.Delete()

   gr_obs = ROOT.TGraph(len(m),m,y_obs)
   gr_exp = ROOT.TGraph(len(m),m,y_exp)
   
   return [gr_obs,gr_exp]

def get_graph_sigma(fname,scale,brs_map):

   f = ROOT.TFile("Limits_%s.root"%(fname))
   grtmp_obs = f.Get("OBSERVED")
   grtmp_exp = f.Get("EXPECTED")
   
   m = array('d',[])
   y_obs = array('d',[])
   y_exp = array('d',[])
   npoints = grtmp_obs.GetN()  
   for p in xrange(0,npoints):
      g_x_obs = ROOT.Double(0.)
      g_y_obs = ROOT.Double(0.)
      grtmp_obs.GetPoint(p,g_x_obs,g_y_obs)
      m.append(g_x_obs)
      idx = int((g_x_obs*1000.-745)/5)
      hvt_br = get_thbrs_from_cadi(fname,idx,brs_map)
      y_obs.append(g_y_obs*scale/hvt_br) 
      g_x_exp = ROOT.Double(0.)
      g_y_exp = ROOT.Double(0.)
      grtmp_exp.GetPoint(p,g_x_exp,g_y_exp)
      idx = int((g_x_exp*1000.-745)/5)
      y_exp.append(g_y_exp*scale/hvt_br) 
      #if fname == 'EXO_14_010' and g_x_obs == 1.8:
      #   print "mass %.1f obs %.5f rescaled %.5f scale %.1f hvt br %.5f" %(g_x_obs,g_y_obs,g_y_obs*scale/hvt_br,scale,hvt_br)     
   
   f.Close()
   f.Delete()

   gr_obs = ROOT.TGraph(len(m),m,y_obs)
   gr_exp = ROOT.TGraph(len(m),m,y_exp)
   
   return [gr_obs,gr_exp]

def get_thbrs_from_cadi(cadi,idx,brs_map):
   
   if cadi == 'EXO_12_025':
      return brs_map['BRZW'][idx]   
      #return brs_map['BRZW'][idx]+brs_map['BRWW'][idx]  
      
   elif cadi == 'EXO_14_010':
      return brs_map['BRWh'][idx]   
      #return brs_map['BRWh'][idx]+brs_map['BRhZ'][idx]  
       
   elif cadi == 'EXO_13_007':
      #return brs_map['BRhZ'][idx]*brs_map['BRWh'][idx]
      #return brs_map['BRhZ'][idx]+brs_map['BRWh'][idx]
      return brs_map['BRhZ'][idx]
      
   elif cadi == 'EXO_14_009_HV':
      #return brs_map['BRhZ'][idx]*brs_map['BRWh'][idx]
      #return brs_map['BRhZ'][idx]+brs_map['BRWh'][idx]
      return brs_map['BRWh'][idx]
      
   elif cadi == 'EXO_12_024':
      #return brs_map['BRWW'][idx]*brs_map['BRZW'][idx]
      #return brs_map['BRWW'][idx]+brs_map['BRZW'][idx]
      return brs_map['BRWW'][idx]
      
   elif cadi == 'EXO_13_009_WW': #or cadi == 'EXO_13_009_ZZ':
      #return brs_map['BRWW'][idx]*brs_map['BRZW'][idx]
      #return brs_map['BRWW'][idx]+brs_map['BRZW'][idx]
      return brs_map['BRWW'][idx]
      
   elif cadi == 'EXO_13_009_ZZ':
      return brs_map['BRZW'][idx]   

def draw_mg(model,thleg,ymin,ymax,ytitle,extratxt,saveas):
   
   dict_ = get_map(model)
   thDict_ = get_theo_map()
   brsDict_ = thDict_[0]
   massDict_ = thDict_[1]

   grs = []

   mg = ROOT.TMultiGraph()
   mg.SetTitle(model)
   leg_limits = get_legend(model) 
   leg_theo = get_legend_theo(model)

   for f in xrange(0,len(dict_['flist'])):
      if model == 'TripletX':
         grs = get_graph_sigma(dict_['flist'][f],dict_['sf'][f],brsDict_)
      else: 
         grs = get_graph(dict_['flist'][f],dict_['sf'][f])
      grs[0].SetMarkerSize(1)
      grs[0].SetLineColor(dict_['palette'][f])
      grs[0].SetLineWidth(dict_['lsize'][f])
      grs[0].SetLineStyle(dict_['lstyle'][f])
      grs[1].SetLineColor(dict_['palette'][f])
      grs[1].SetLineWidth(2)
      grs[1].SetLineStyle(3)
      if opts.doexp:
   	 grs[1].SetLineStyle(dict_['lstyle'][f])
   	 grs[1].SetLineWidth(dict_['lsize'][f])
   	 leg_limits[f*2/len(dict_['flist'])].AddEntry(grs[1],dict_['leg'][f],"L")
	 mg.Add(grs[1])
      if not opts.doexp:    
   	 mg.Add(grs[0])
   	 leg_limits[f*2/len(dict_['flist'])].AddEntry(grs[0],dict_['leg'][f],"L")
      #mg.Add(grs[1])
  
   grs.append(get_theo_gr(model,brsDict_,massDict_))
   grs[2].SetLineWidth(3)
   grs[2].SetLineColor(ROOT.TColor.kBlack)
   grs[2].SetLineStyle(7)
   mg.Add(grs[2])
   leg_limits[1].AddEntry(grs[2],thleg,"L")
   #leg_theo.AddEntry(grs[2],thleg,"L")
      
   canv = get_canvas("c")
   canv.cd()

   mg.SetMinimum(ymin)
   mg.SetMaximum(ymax)
   mg.Draw("AL")
   mg.GetXaxis().SetTitle("Resonance mass [TeV]")
   mg.GetYaxis().SetTitle(ytitle)
   mg.GetYaxis().CenterTitle()
   mg.GetXaxis().CenterTitle()
   mg.GetYaxis().SetTitleSize(0.06)
   mg.GetXaxis().SetTitleSize(0.06)
   mg.GetXaxis().SetLabelSize(0.045)
   mg.GetYaxis().SetLabelSize(0.045)
   mg.GetYaxis().SetTitleOffset(1.1)
   mg.GetXaxis().SetTitleOffset(0.9)   

   ptfake = ROOT.TPaveText(0.45,0.57,0.93,0.88,"NDC")
   ptfake.SetFillColor(0)
   ptfake.SetBorderSize(0)
   ptfake.Draw()
   
   leg_theo.Draw()
   for l in leg_limits:
      l.Draw()
   
   if extratxt:
      if model != 'TripletX':
      	 pt = ROOT.TPaveText(0.16,0.15,0.49,0.24,"NDC")
	 pt.SetFillColor(0)
      	 pt.AddText("HVT Model B (g_{V} = 3)")
      else:
         pt = ROOT.TPaveText(0.14,0.14,0.35,0.23,"NDC")
	 text = pt.AddText("HVT Model B (g_{V} = 3)")
	 text.SetTextFont(62)
	 pt.AddText("BR(X#rightarrowWZ) #approx BR(X#rightarrowWH)")
	 pt.AddText(" #approx BR(X#rightarrowWW) #approx BR(X#rightarrowZH)")
      pt.SetTextFont(42)
      pt.SetTextSize(0.0246114)
      pt.SetTextAlign(12)
      pt.SetFillColor(0)
      pt.SetBorderSize(0)
      pt.SetFillStyle(0)      
      pt.Draw()
   
      pt2 = ROOT.TPaveText(0.63,0.52,0.93,0.58,"NDC")
      pt2.AddText("X = X^{#pm} / X^{0} , V = W / Z")
      #pt2.AddText("V = W / Z")
      pt2.SetTextFont(62)
      pt2.SetTextSize(0.0246114)
      pt2.SetTextAlign(31)
      pt2.SetFillColor(0)
      pt2.SetBorderSize(0)
      pt2.Draw()      
      
   #if model == 'TripletX':
   #   xsec_measure = get_xsec_measure()
   #   xsec_measure.SetMarkerColor(kBlack)
   #   xsec_measure.SetMarkerStyle(20)
   #   xsec_measure.SetMarkerSize(1.2)
   #   xsec_measure.SetLineWidth(2)
   #   xsec_measure.Draw("Psame")
   #   pt2 = ROOT.TPaveText(0.21,0.78,0.42,0.88,"NDC")
   #   pt2.AddText("EXO-14-010")
   #   pt2.AddText("Cross-section measurement")
   #   pt2.AddText("with MaxLikelihoodFit @ 1.8 TeV")
   #   pt2.SetTextFont(42)
   #   pt2.SetTextSize(0.03)
   #   pt2.SetTextAlign(12)
   #   pt2.SetFillColor(0)
   #   pt2.SetBorderSize(0)
   #   pt2.SetFillStyle(0)      
   #   pt2.Draw()
           
   canv.Update()

   canv.cd()
   CMS_lumi.CMS_lumi(canv, 2, 0)	   
   canv.cd()
   canv.Update()
   canv.RedrawAxis()
   frame = canv.GetFrame()
   frame.Draw()   
   canv.cd()
   canv.Update()
   #canv.SaveAs("%s.pdf"%(saveas),"pdf")
   
   canv.SaveAs("%s.pdf"%(saveas),"pdf")
   time.sleep(10000)
   grs[0].Delete()
   grs[1].Delete()
   grs[2].Delete()   
   mg.Delete()
   leg_limits.Delete()
   leg_theo.Delete()
   if extratxt:
      pt.Delete()
   canv.Close()

def get_xsec_measure():

   rfit = 0.019347#0.029130
   errp = 0.013567#0.032602
   errm = 0.009817#0.005092
   x = array('d',[0.85,1.8])
   y = array('d',[10,rfit*1.5/0.48075])
   xl = array('d',[0.,0.])
   xh = array('d',[0.,0.])
   yl = array('d',[0.,errm*1.5/0.48075])
   yh = array('d',[0.,errp*1.5/0.48075])
   #yl = array('d',[(rfit*1.5/0.48075-errm*1.5/0.48075)])
   #yh = array('d',[(errp*1.5/0.48075-rfit*1.5/0.48075)])
      
   gr_xsec_m = ROOT.TGraphAsymmErrors(2,x,y,xl,xh,yl,yh)
   #gr_xsec_m = SetPointEYhigh(0,1.50224)
   #gr_xsec_m = SetPointEYlow(0,1.08702)
   
   return gr_xsec_m
   
## main code ##
argv = sys.argv
parser = OptionParser()
parser.add_option("-c", "--convert", dest="convert", default=False, action="store_true",
                              help="convert files")
parser.add_option("-e", "--exp", dest="doexp", default=False, action="store_true",
                              help="plot only expected limits")
			      			      			      			      
(opts, args) = parser.parse_args(argv)

if opts.convert:
   print "### converting files ###"
   convert_files()
 
models_ = ['SingletXpm','SingletX0','TripletXpm','TripletX0','TripletX']
thleg_ = ['pp #rightarrow X^{#pm} #rightarrow WZ/WH','pp #rightarrow X^{0} #rightarrow WW/ZH',
          'pp #rightarrow X^{#pm} #rightarrow WZ/WH','pp #rightarrow X^{0} #rightarrow WW/ZH','#sigma_{TH}(pp #rightarrow X^{+})+#sigma_{TH}(pp #rightarrow X^{-})+#sigma_{TH}(pp #rightarrow X^{0})']#'pp #rightarrow X']
mg_ymin = [0.0001,0.0001,0.0001,0.0001,0.005]
mg_ymax = [30,30,30,30,6]
mg_ytitle = ['#sigma(pp#rightarrow X^{#pm}) #times B(X^{#pm} #rightarrow WZ/WH) [pb]','#sigma(pp#rightarrow X^{0}) #times B(X^{0} #rightarrow WW/ZH) [pb]',
             '#sigma(pp#rightarrow X^{#pm}) #times B(X^{#pm} #rightarrow WZ/WH) [pb]','#sigma(pp#rightarrow X^{0}) #times B(X^{0} #rightarrow WW/ZH) [pb]',
	     '#sigma_{95%}(pp #rightarrow X) [pb]'] 
extra_txt = [False,False,True,True,True]
save = ['EXOVVVHLimitsCombined_SigmaBR_Wp_Singlet','EXOVVVHLimitsCombined_SigmaBR_Zp_Singlet',
        'EXOVVVHLimitsCombined_SigmaBR_Wp_Triplet','EXOVVVHLimitsCombined_SigmaBR_Zp_Triplet','EXOVVVHLimitsCombined_Sigma_Triplet']

for e in xrange(4,len(models_)):
   print "======================= %s ========================" %(models_[e])
   draw_mg(models_[e],thleg_[e],mg_ymin[e],mg_ymax[e],mg_ytitle[e],extra_txt[e],save[e])

