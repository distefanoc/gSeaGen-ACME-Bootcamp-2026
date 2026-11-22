import ROOT
import os
import math

ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")

os.makedirs("plots", exist_ok=True)

# Input file
f = ROOT.TFile.Open("files/honda_real.1.et.root")
header = f.Get("Header")
tree = f.Get("Events")

# Generation parameters
header.GetEntry(0)
gp = header.Header

emin = gp.EvMin
emax = gp.EvMax

# Livetime in seconds
livetime = 86400.
scale = 7

# Book energy histograms
hE = ROOT.TH1D("hE", "", 40,
              math.log10(emin), math.log10(emax))

hEweighted = ROOT.TH1D("hEweighted", "", 40,
                      math.log10(emin), math.log10(emax))

hE.Sumw2()
hEweighted.Sumw2()

# Loop over events
for entry in tree:
    event = entry.Events
    nu = event.Tracks[0]

    energy = math.log10(nu.E)

    # Generated events
    hE.Fill(energy)

    # Constant event weight
    hEweighted.Fill(energy, scale)

# Scale the original histogram
hEscaled = hE.Clone("hEscaled")
hEscaled.Scale(scale)

# Histogram style
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetFrameLineWidth(3)

ymin = 1
ymax = 1E4

for h in [hE, hEscaled, hEweighted]:
    h.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
    h.GetYaxis().SetTitle("Events")
    h.SetLineWidth(2)
    h.SetMinimum(ymin)
    h.SetMaximum(ymax)

hE.SetLineColor(ROOT.kBlack)
hE.SetLineWidth(3)

hEscaled.SetLineColor(ROOT.kRed)
hEscaled.SetLineStyle(1)
hEscaled.SetLineWidth(3)

hEweighted.SetLineColor(ROOT.kGreen + 2)
hEweighted.SetLineStyle(2)
hEweighted.SetLineWidth(4)

# Plot 1: generated events
c1 = ROOT.TCanvas("c1", "Generated events", 700, 500)
c1.SetLogy()

hE.Draw("HIST")

leg1 = ROOT.TLegend(0.55, 0.82, 0.88, 0.88)
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)
leg1.SetTextSize(0.035)
leg1.AddEntry(hE, "Generated events", "l")
leg1.Draw()

c1.Update()
c1.SaveAs("plots/honda_real_1day.png")

# Plot 2: generated and scaled events
c2 = ROOT.TCanvas("c2", "Scaled events", 700, 500)
c2.SetLogy()

hE.Draw("HIST")
hEscaled.Draw("HIST SAME")

leg2 = ROOT.TLegend(0.55, 0.76, 0.88, 0.88)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
leg2.SetTextSize(0.035)
leg2.AddEntry(hE, "Generated events", "l")
leg2.AddEntry(hEscaled, "Scaled events", "l")
leg2.Draw()

c2.Update()
c2.SaveAs("plots/honda_real_rate_scaled.png")

# Plot 3: generated, scaled and weighted events
c3 = ROOT.TCanvas("c3", "Weighted events", 700, 500)
c3.SetLogy()

hE.Draw("HIST")
hEscaled.Draw("HIST SAME")
hEweighted.Draw("HIST SAME")

leg3 = ROOT.TLegend(0.55, 0.70, 0.88, 0.88)
leg3.SetBorderSize(0)
leg3.SetFillStyle(0)
leg3.SetTextSize(0.035)
leg3.AddEntry(hE, "Generated events", "l")
leg3.AddEntry(hEscaled, "Scaled events", "l")
leg3.AddEntry(hEweighted, "Weighted events", "l")
leg3.Draw()

c3.Update()
c3.SaveAs("plots/honda_real_rate_weighted.png")

# Integrated results
print(f"Simulated livetime: {livetime:.0f} s")
print(f"Target livetime: {livetime * scale:.0f} s")
print(f"Simulated events: {tree.GetEntries()}")
print(f"Events in 1 day: {hE.Integral():.0f}")
print(f"Event weight: {scale:.0f}")
print(f"Events in 1 week (scaled): {hEscaled.Integral():.0f}")
print(f"Events in 1 week (weighted): {hEweighted.Integral():.0f}")

input("Press Enter to exit...")
