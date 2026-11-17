import ROOT
import os
import sys
import math

ROOT.gROOT.SetBatch(not bool(os.environ.get("DISPLAY")))
ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")

# Input file
filename = sys.argv[1]
name = os.path.basename(filename).replace(".et.root", "")

f = ROOT.TFile.Open(filename)
header = f.Get("Header")
tree = f.Get("Events")

# Generation parameters
header.GetEntry(0)
gp = header.Header

ntot = gp.NTot
emin = gp.EvMin
emax = gp.EvMax
ctmin = gp.CtMin
ctmax = gp.CtMax

# Book energy histograms
hE = ROOT.TH1D("hE", "Unweighted events", 40,
              math.log10(emin), math.log10(emax))

hEw = ROOT.TH1D("hEw", "Weighted events", 40,
               math.log10(emin), math.log10(emax))

# Book zenith angle histograms
hCt = ROOT.TH1D("hCt", "Unweighted events", 40,
               ctmin, ctmax)

hCtw = ROOT.TH1D("hCtw", "Weighted events", 40,
                ctmin, ctmax)

# Axis titles
hE.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
hE.GetYaxis().SetTitle("MC events")

hEw.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
hEw.GetYaxis().SetTitle("Event rate (Hz)")

hCt.GetXaxis().SetTitle("cos#theta_{#nu}")
hCt.GetYaxis().SetTitle("MC events")

hCtw.GetXaxis().SetTitle("cos#theta_{#nu}")
hCtw.GetYaxis().SetTitle("Event rate (Hz)")

# Enable calculation of weighted statistical errors
hEw.Sumw2()
hCtw.Sumw2()

# Loop over events
for entry in tree:
    event = entry.Events
    nu = event.Tracks[0]

    weight = event.EvtWeight / ntot

    # Unweighted distributions
    hE.Fill(math.log10(nu.E))
    hCt.Fill(nu.D3)

    # Weighted distributions
    hEw.Fill(math.log10(nu.E), weight)
    hCtw.Fill(nu.D3, weight)

# Histogram style
ROOT.gStyle.SetOptStat(0)

for h in [hE, hCt]:
    h.SetLineColor(ROOT.kBlue)
    h.SetLineWidth(2)

for h in [hEw, hCtw]:
    h.SetLineColor(ROOT.kRed)
    h.SetMarkerColor(ROOT.kRed)
    h.SetLineWidth(2)

# Draw energy distributions
cE = ROOT.TCanvas("cE", "Neutrino energy", 1200, 500)
cE.Divide(2, 1)

cE.cd(1)
hE.Draw("HIST")

cE.cd(2)
hEw.Draw("HIST E")

cE.Update()
cE.SaveAs("plots/" + name + "_nu_energy.png")

# Draw zenith angle distributions
cCt = ROOT.TCanvas("cCt", "Neutrino zenith angle", 1200, 500)
cCt.Divide(2, 1)

cCt.cd(1)
hCt.Draw("HIST")

cCt.cd(2)
hCtw.Draw("HIST E")

cCt.Update()
cCt.SaveAs("plots/" + name + "_nu_costheta.png")


print("Generation parameters:")
print(f"  Mean number of neutrinos to simulate: {ntot:.0f}")
print(f"  Energy range: {emin:.2e} - {emax:.2e} GeV")
print(f"  Cosine of zenith range: {ctmin} - {ctmax}")
print(f"  Number of energy bins: {gp.NBin}")
print(f"  Number of saved events: {tree.GetEntries()}")


# Print integrated results
print(f"Total MC events: {hE.Integral():.0f}")
print(f"Total event rate: {hEw.Integral():.4e} Hz")
print(f"Expected events per year: {hEw.Integral()*365.25*86400:.2f}")
