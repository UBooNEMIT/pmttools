import os,sys
import ROOT as rt

trignames = {"BNB":{"algo":"BNB_FEMBeamTriggerAlgo",
                    "prescale":"BNB_unbiased_PrescaleAlgo"}}

def make_trigrate_hist( name, rootfile, trigtype="BNB" ):
    histname = "h%s_%s"%(name,trigtype)
    hall  = rt.TH1D(histname+"_all",";effective PE (PHMAX/20);frac",100,0,50)
    hpass = rt.TH1D(histname+"_pass",";effective PE (PHMAX/20);frac",100,0,50)
    hpres = rt.TH1D(histname+"_prescale",";effective PE (PHMAX/20);frac",100,0,50)
    hfrac = rt.TH1D(histname,";effective PE (PHMAX/20);fraction passed",100,0,50)

    fin = rt.TFile(rootfile)
    fem = fin.Get("femsoft/swtrigdata")

    nentries = fem.GetEntries()
    fem.GetEntry(0)
    first_tstamp = fem.event_timestamp_sec + 1.0e-6*fem.event_timestamp_usec
    last_tstamp = first_tstamp
    for entry in range(0,nentries):
        fem.GetEntry(entry)
        ntrigs = fem.algonames.size()

        # Get the trig type we want
        if trigtype=="BNB" and fem.bnb!=1:
            continue

        PHMAX = 0
        sw_pass = 0
        pre_pass = 0
        for itrig in range(0,ntrigs):
            if trignames[trigtype]["algo"]==fem.algonames.at(itrig):
                # Algo trig
                PHMAX = fem.PHMAX.at(itrig)
                sw_pass = fem.swtrigpass.at(itrig)
            elif trignames[trigtype]["prescale"]==fem.algonames.at(itrig):
                # Pre-scale
                pre_pass = fem.algopass.at(itrig)
                
        hall.Fill( PHMAX/20.0 )
        if sw_pass==1:
            hpass.Fill( PHMAX/20.0 )
        else:
            if pre_pass==1:
                hpres.Fill( PHMAX/20.0 )

        tstamp = fem.event_timestamp_sec + 1.0e-6*fem.event_timestamp_usec
        if tstamp>last_tstamp:
            last_tstamp = tstamp
        else:
            print "out of order time stamp"
            
    print "Filled: ",hpass.Integral(),hpres.Integral()
    telapsed = last_tstamp-first_tstamp
    print "Time Elapsed: ",telapsed
    hpres.Scale( 1.0/0.0026 )
    hpres.Scale( 1.0/telapsed )
    hpass.Scale( 1.0/telapsed )
    return hpass,hpres


if __name__ == "__main__":

    filelist = []

    print len(sys.argv)
    for x in range(1,len(sys.argv)):
        filelist.append( sys.argv[x] )

    print "Files to process: ",filelist

    c = rt.TCanvas("c","c",800,600)
    c.Draw()
    ifile = "file1"
    hpass, hpre = make_trigrate_hist( ifile, filelist[0] )
    hpre.SetLineColor(rt.kBlack)
    hpre.Draw()
    hpass.Draw("same")
    hpre.GetYaxis().SetRangeUser(1.0e-4,0.1e2)
    c.SetLogy(1)
    raw_input()

