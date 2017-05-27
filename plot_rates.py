import os,sys

import ROOT as rt

rt.gStyle.SetOptStat(0)
rt.gStyle.SetTitleFontSize(0.2)
rt.gStyle.SetLabelSize(0.05,"X")
rt.gStyle.SetPadBottomMargin(0.15)

input = sys.argv[1]
fin = rt.TFile(input,"open")
tree = fin.Get("specalib/eventtree")

cut = "chmaxamp<2048+300"
nbins = 20
window = 15.625e-9*1500.0

print "INPUT FILE: ",input

# Rates for each channel
hrate = rt.TH1D("hrate",";FEMCH;kHz",32,0,32)

# first, get npulse distribution for each pmt
poiseq = "[0]*TMath::Power([1],x)*TMath::Exp(-[1])/TMath::Gamma(x+1.0)"
c = rt.TCanvas("c","Pulse per Beam Window",1200,1200)
c.Draw()
hpmts = {}
hfits = {}
c.Divide(6,6)
for ipmt in range(0,32):
    htemp = rt.TH1D("hnpulses_%d"%(ipmt),"",nbins,0,nbins)
    c.cd(ipmt+1)
    tree.Draw("nchfires[%d]>>hnpulses_%d"%(ipmt,ipmt),cut)

    mean = htemp.GetMean()
    amp  = htemp.GetMaximum()
    
    f1 = rt.TF1("f1_%d"%(ipmt),poiseq,0,nbins)
    f1.SetParameter(0,amp)
    f1.SetParameter(1,mean)
    htemp.Fit( f1, "RQ","",0,nbins)

    r = f1.GetParameter(1)/window*1.0e-3 # kHz

    hrate.SetBinContent(ipmt+1,r)
    #htemp.SetBinContent(ipmt+1,htemp.GetMean())
    #htemp.GetXaxis().SetNdivisions(505)
    hpmts[ipmt] = htemp
    hfits[ipmt] = f1
    c.Update()

hrate.SetMinimum(0)
hrate.SetMaximum(400)
for ch in range(32):
    hrate.GetXaxis().SetBinLabel(ch+1,"%d"%(ch))
crate = rt.TCanvas("crate","Rate per PMT",1400,600)
crate.SetGridy(1)
crate.SetGridx(1)
hrate.SetLineWidth(4)
hrate.GetXaxis().SetTitleSize(0.05)
hrate.Draw("hist")
crate.Update()

raw_input()
    
    
    
