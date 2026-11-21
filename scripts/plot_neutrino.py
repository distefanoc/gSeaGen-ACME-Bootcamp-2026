import ROOT
import os
import sys
import math

# Use graphical mode when a display is available; otherwise run without windows.
ROOT.gROOT.SetBatch(not bool(os.environ.get("DISPLAY")))
# Load the gSeaGen event classes so ROOT can read the stored objects.
ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")

# Read the ROOT file name from the command line.
filename = sys.argv[1]
name = os.path.basename(filename).replace(".et.root", "")

# The Header tree stores generation settings; Events stores simulated events.
f = ROOT.TFile.Open(filename)
header = f.Get("Header")
tree = f.Get("Events")

# Read the first Header entry to obtain the simulated energy and angle ranges
# and the number of neutrinos used for normalisation.
header.GetEntry(0)
gp = header.Header

ntot = gp.NTot
emin = gp.EvMin
emax = gp.EvMax
ctmin = gp.CtMin
ctmax = gp.CtMax

# Use log10(E/GeV) to display the broad neutrino energy range.
# Create separate histograms for event counts and weighted event rates.
hE = ROOT.TH1D("hE", "Unweighted events", 40,
              math.log10(emin), math.log10(emax))

hEw = ROOT.TH1D("hEw", "Weighted events", 40,
               math.log10(emin), math.log10(emax))

# The angular distributions use the cosine of the neutrino zenith angle.
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

# Store the sum of squared weights for statistical uncertainties
# in the weighted histograms.
hEw.Sumw2()
hCtw.Sumw2()

# Loop over saved events; the first track contains the incoming neutrino.
for entry in tree:
    event = entry.Events
    nu = event.Tracks[0]

    # Divide the event weight by the number of generated neutrinos:
    # each weighted entry contributes to the estimated event rate in Hz.
    weight = event.EvtWeight / ntot

    # Each saved event contributes one count to these distributions.
    hE.Fill(math.log10(nu.E))
    hCt.Fill(nu.D3)

    # Each event contributes its normalised weight to the rate distributions.
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

# Draw event counts and estimated event rates side by side.
cE = ROOT.TCanvas("cE", "Neutrino energy", 1200, 500)
cE.Divide(2, 1)

cE.cd(1)
hE.Draw("HIST")

cE.cd(2)
hEw.Draw("HIST E")

cE.Update()
cE.SaveAs("plots/" + name + "_nu_energy.png")

# Draw the corresponding distributions in cos(zenith angle).
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


# Integrating the weighted energy histogram gives the total rate in Hz.
# Multiply by the number of seconds in a year to estimate annual events.
print(f"Total MC events: {hE.Integral():.0f}")
print(f"Total event rate: {hEw.Integral():.4e} Hz")
print(f"Expected events per year: {hEw.Integral()*365.25*86400:.2f}")
