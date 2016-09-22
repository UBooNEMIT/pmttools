import os,sys

import ROOT as rt

rt.gStyle.SetOptStat(0)
rt.gStyle.SetTitleFontSize(0.2)
rt.gStyle.SetLabelSize(0.1,"X")

input = sys.argv[1]
fin = rt.TFile(input,"open")
tree = fin.Get("specalib/pulsetree")

cut = "chmaxamp<2048+300 && opchannel==%d && baselinerms<10.0 && baselinerms2<10.0"

print "INPUT FILE: ",input

hamp = rt.TH1D("hamp","",32,0,32)

c = rt.TCanvas("c","c",1200,1200)
hpmts = {}
c.Divide(6,6)
for ipmt in range(0,32):
    htemp = rt.TH1D("hamp_%d"%(ipmt),"",50,0,50)
    c.cd(ipmt+1)
    tree.Draw("maxamp>>hamp_%d"%(ipmt),"chmaxamp<2048+300 && opchannel==%d && baselinerms<10.0 && baselinerms2<10.0"%(ipmt))
    c.Update()
    hamp.SetBinContent(ipmt+1,htemp.GetMean())
    hamp.GetXaxis().SetNdivisions(505)
    hamp.GetXaxis().SetBinLabel(ipmt+1,"femch%02d"%(ipmt))
    hamp.GetXaxis().SetLabelSize(0.05)
    hpmts[ipmt] = htemp

cmean = rt.TCanvas("cmean","",1200,400)
cmean.Draw()
hamp.Draw()
cmean.Update()

c2d = rt.TCanvas("c2d","c2d",1200,1200)
hpmts2d = {}
lines = []
c2d.Divide(6,6)
for ipmt in range(0,32):
    htemp = rt.TH2D("h2d_%d"%(ipmt),"FEMCH%d"%(ipmt),30,0,300, 50,0,50)
    c2d.cd(ipmt+1)
    c2d.cd(ipmt+1).SetTopMargin(0.15)
    tree.Draw("maxamp:charge>>h2d_%d"%(ipmt),cut%(ipmt),"COLZ")
    htemp.GetXaxis().SetNdivisions(505)
    htemp.GetXaxis().SetLabelSize(0.1)
    htemp.GetYaxis().SetNdivisions(505)
    htemp.GetYaxis().SetLabelSize(0.1)    
    htemp.SetTitleSize(60)
    tl = rt.TLine(0,10,300,10)
    tl.SetLineStyle(2)
    tl.Draw()
    tt = rt.TLine(0,20,300,20)
    tt.SetLineStyle(2)
    tt.SetLineColor(rt.kRed)
    tt.Draw()
    c2d.Update()
    hpmts2d[ipmt+1] = htemp
    lines.append( tl )
    lines.append( tt )
c2d.Update()

raw_input()
    
    
    
