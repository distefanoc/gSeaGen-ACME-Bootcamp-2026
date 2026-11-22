
import ROOT
import os
import math

ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")

os.makedirs("plots", exist_ok=True)

# Input files
freal = ROOT.TFile.Open("files/honda_real.1.et.root")
fwgt = ROOT.TFile.Open("files/honda_weighted.1.et.root")

treal = freal.Get("Events")
twgt = fwgt.Get("Events")

# Generation parameters
header = fwgt.Get("Header")
header.GetEntry(0)
gp = header.Header

ntot = gp.NTot
emin = gp.EvMin
emax = gp.EvMax
ctmin = gp.CtMin
ctmax = gp.CtMax

# Livetime in seconds
livetime = 86400.

# Number of histogram bins
nbins = 40

# Book energy histograms
hEreal = ROOT.TH1D("hEreal", "", nbins,
                  math.log10(emin), math.log10(emax))

hEwgt = ROOT.TH1D("hEwgt", "", nbins,
                 math.log10(emin), math.log10(emax))

hEgen = ROOT.TH1D("hEgen", "", nbins,
                 math.log10(emin), math.log10(emax))

# Book zenith angle histograms
hCtreal = ROOT.TH1D("hCtreal", "", nbins, ctmin, ctmax)
hCtwgt = ROOT.TH1D("hCtwgt", "", nbins, ctmin, ctmax)
hCtgen = ROOT.TH1D("hCtgen", "", nbins, ctmin, ctmax)

# Separate histograms for nu_mu (14) and anti-nu_mu (-14)
species = {14: "nu_mu", -14: "anti_nu_mu"}
histograms = {
    "Ereal": hEreal, "Ewgt": hEwgt, "Egen": hEgen,
    "Ctreal": hCtreal, "Ctwgt": hCtwgt, "Ctgen": hCtgen,
}
by_pdg = {}
for pdg, label in species.items():
    by_pdg[pdg] = {
        "Ereal": ROOT.TH1D(f"hEreal_{label}", "", nbins, math.log10(emin), math.log10(emax)),
        "Ewgt": ROOT.TH1D(f"hEwgt_{label}", "", nbins, math.log10(emin), math.log10(emax)),
        "Egen": ROOT.TH1D(f"hEgen_{label}", "", nbins, math.log10(emin), math.log10(emax)),
        "Ctreal": ROOT.TH1D(f"hCtreal_{label}", "", nbins, ctmin, ctmax),
        "Ctwgt": ROOT.TH1D(f"hCtwgt_{label}", "", nbins, ctmin, ctmax),
        "Ctgen": ROOT.TH1D(f"hCtgen_{label}", "", nbins, ctmin, ctmax),
    }

for h in list(histograms.values()) + [
    h for group in by_pdg.values() for h in group.values()
]:
    h.Sumw2()

# REAL mode
for entry in treal:
    event = entry.Events
    nu = event.Tracks[0]
    energy = math.log10(nu.E)
    costheta = nu.D3

    hEreal.Fill(energy)
    hCtreal.Fill(costheta)

    if nu.PdgCode in by_pdg:
        by_pdg[nu.PdgCode]["Ereal"].Fill(energy)
        by_pdg[nu.PdgCode]["Ctreal"].Fill(costheta)

# Weighted mode
for entry in twgt:
    event = entry.Events
    nu = event.Tracks[0]
    energy = math.log10(nu.E)
    costheta = nu.D3

    # Before weighting
    hEgen.Fill(energy)
    hCtgen.Fill(costheta)

    if nu.PdgCode in by_pdg:
        by_pdg[nu.PdgCode]["Egen"].Fill(energy)
        by_pdg[nu.PdgCode]["Ctgen"].Fill(costheta)

    # After weighting: original normalization unchanged
    weight = event.EvtWeight / ntot * livetime

    hEwgt.Fill(energy, weight)
    hCtwgt.Fill(costheta, weight)

    if nu.PdgCode in by_pdg:
        by_pdg[nu.PdgCode]["Ewgt"].Fill(energy, weight)
        by_pdg[nu.PdgCode]["Ctwgt"].Fill(costheta, weight)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetFrameLineWidth(2)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

colors = {None: ROOT.kBlack, 14: ROOT.kRed, -14: ROOT.kGreen + 2}
for pdg, group in [(None, histograms)] + list(by_pdg.items()):
    for key, h in group.items():
        color = colors[pdg]
        h.SetLineColor(color)
        h.SetMarkerColor(color)
        h.SetLineWidth(2)
        if key.endswith("real"):
            h.SetMarkerStyle(20)
            h.SetMarkerSize(0.55)
        h.GetXaxis().SetTitle(
            "log_{10}(E_{#nu}/GeV)" if key.startswith("E") else "cos#theta_{#nu}"
        )
        h.GetYaxis().SetTitle("Events" if key.endswith("gen") else "Events / day")
        h.GetXaxis().SetTitleSize(0.045)
        h.GetYaxis().SetTitleSize(0.045)
        h.GetXaxis().SetLabelSize(0.040)
        h.GetYaxis().SetLabelSize(0.040)
        h.GetYaxis().SetTitleOffset(1.2)
        h.GetXaxis().SetTitleOffset(1.1)

legends = []

def set_pad_style():
    ROOT.gPad.SetLeftMargin(0.13)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gPad.SetBottomMargin(0.13)
    ROOT.gPad.SetTopMargin(0.06)

def make_legend():
    leg = ROOT.TLegend(0.64, 0.72, 0.94, 0.92)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.033)
    legends.append(leg)
    return leg

def draw_generated(key):
    set_pad_style()
    total = histograms[key]
    nu = by_pdg[14][key]
    antinu = by_pdg[-14][key]
    total.SetMinimum(0)
    total.SetMaximum(1.25 * max(h.GetMaximum() for h in (total, nu, antinu)))
    total.Draw("HIST")
    nu.Draw("HIST SAME")
    antinu.Draw("HIST SAME")

    leg = make_legend()
    leg.SetHeader("UNWEIGHTED")
    leg.AddEntry(total, "Total", "l")
    leg.AddEntry(nu, "#nu_{#mu} (14)", "l")
    leg.AddEntry(antinu, "#bar{#nu}_{#mu} (-14)", "l")
    leg.Draw()

def draw_comparison(real_key, weighted_key):
    set_pad_style()
    real = [histograms[real_key], by_pdg[14][real_key], by_pdg[-14][real_key]]
    weighted = [histograms[weighted_key], by_pdg[14][weighted_key], by_pdg[-14][weighted_key]]
    real[0].SetMinimum(0)
    real[0].SetMaximum(1.25 * max(h.GetMaximum() for h in real + weighted))
    real[0].Draw("E1")
    for h in weighted:
        h.Draw("HIST SAME")
    for h in real:
        h.Draw("E1 SAME")

    leg = make_legend()
    leg.AddEntry(real[0], "REAL (points)", "lep")
    leg.AddEntry(weighted[0], "WEIGHTED (lines)", "l")
    leg.AddEntry(weighted[1], "#nu_{#mu} (14)", "l")
    leg.AddEntry(weighted[2], "#bar{#nu}_{#mu} (-14)", "l")
    leg.Draw()

# One canvas with four panels
c = ROOT.TCanvas("c", "REAL vs WEIGHTED", 1200, 1000)
c.Divide(2, 2)

c.cd(1)
draw_generated("Egen")
c.cd(2)
draw_comparison("Ereal", "Ewgt")
c.cd(3)
draw_generated("Ctgen")
c.cd(4)
draw_comparison("Ctreal", "Ctwgt")

c.Update()
c.SaveAs("plots/honda_comparison_4plots.png")

print("Generation parameters (weighted mode):")
print(f"  Number of generated neutrinos: {ntot:.0f}")
print(f"  Energy range: {emin:.2e} - {emax:.2e} GeV")
print(f"  Cosine of zenith range: {ctmin} - {ctmax}")
print(f"  Number of energy bins: {gp.NBin}")

print()
print("REAL mode:")
print(f"  Number of saved events: {treal.GetEntries()}")
print(f"  Events per day: {hEreal.Integral():.2f}")
print(f"  Event rate: {hEreal.Integral()/livetime:.4e} Hz")

print()
print("Weighted mode:")
print(f"  Number of saved events: {twgt.GetEntries()}")
print(f"  Events before weighting: {hEgen.Integral():.0f}")
print(f"  Events per day: {hEwgt.Integral():.2f}")
print(f"  Event rate: {hEwgt.Integral()/livetime:.4e} Hz")

print()
if hEreal.Integral() > 0:
    print(f"Weighted/REAL ratio: {hEwgt.Integral()/hEreal.Integral():.4f}")

input("Press Enter to exit...")
