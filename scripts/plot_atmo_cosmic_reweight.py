import ROOT
import os
import math
from atmospheric_flux import atmospheric_numu_flux

ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")
os.makedirs("plots", exist_ok=True)

filename = "files/atmo_cosmic_reweight.1.et.root"
f = ROOT.TFile.Open(filename)
if not f or f.IsZombie():
    raise RuntimeError(f"Cannot open {filename}")

tree = f.Get("Events")
header = f.Get("Header")
if not tree or not header or header.GetEntries() == 0:
    raise RuntimeError("Missing Events or Header tree")
header.GetEntry(0)
ntot = float(header.Header.NTot)
emin = float(header.Header.EvMin)
emax = float(header.Header.EvMax)
if ntot <= 0 or emin <= 0 or emax <= emin:
    raise RuntimeError("Invalid generation parameters in Header")

nbins = 40
species = {None: "total", 14: "numu", -14: "antinumu"}
colors = {None: ROOT.kBlack, 14: ROOT.kRed, -14: ROOT.kGreen + 2}
hist = {}
for model in ("cosmic", "atmo"):
    for pdg, label in species.items():
        h = ROOT.TH1D(f"h_{model}_{label}", "", nbins,
                      math.log10(emin), math.log10(emax))
        h.Sumw2()
        h.SetDirectory(0)
        hist[(model, pdg)] = h

# Fill both physical hypotheses from the same diffuse Monte Carlo sample.
for entry in tree:
    event = entry.Events
    nu = event.Tracks[0]
    pdg = int(nu.PdgCode)
    if pdg not in (14, -14) or not (emin <= nu.E < emax):
        continue

    x = math.log10(nu.E)
    # Cosmic: use the FUNC1 E^-2 flux already specified by -f at generation.
    cosmic_weight = event.EvtWeight / ntot
    # Atmospheric: replace the generation flux with Wang-Yasuda.
    atmo_flux = atmospheric_numu_flux(nu.E, nu.D3, pdg)
    atmo_weight = event.GenWeight / ntot * atmo_flux

    for key in (None, pdg):
        hist[("cosmic", key)].Fill(x, cosmic_weight)
        hist[("atmo", key)].Fill(x, atmo_weight)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

for pdg in species:
    for model in ("cosmic", "atmo"):
        h = hist[(model, pdg)]
        h.SetLineColor(colors[pdg])
        h.SetMarkerColor(colors[pdg])
        h.SetLineWidth(2)
        if model == "cosmic":
            h.SetMarkerStyle(20)
            h.SetMarkerSize(0.6)

c = ROOT.TCanvas("c_atmo_cosmic", "Atmospheric vs cosmic reweighting", 1000, 650)
c.cd()
ROOT.gPad.SetLeftMargin(0.13)
ROOT.gPad.SetRightMargin(0.05)
ROOT.gPad.SetBottomMargin(0.12)
ROOT.gPad.SetTopMargin(0.06)
ROOT.gPad.SetLogy()

positive = [h.GetBinContent(i) for h in hist.values()
            for i in range(1, nbins + 1) if h.GetBinContent(i) > 0]
minimum = min(positive) if positive else 1e-30
maximum = max(h.GetMaximum() for h in hist.values())
frame = hist[("cosmic", None)]
frame.SetTitle("Cosmic vs atmospheric flux")
frame.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
frame.GetYaxis().SetTitle("Event rate (Hz / bin)")
frame.GetYaxis().SetTitleOffset(1.4)
frame.SetMinimum(max(minimum * 0.3, 1e-30))
frame.SetMaximum(maximum * 5 if maximum > 0 else 1)
frame.Draw("E1")
for pdg in species:
    hist[("atmo", pdg)].Draw("HIST SAME")
for pdg in species:
    hist[("cosmic", pdg)].Draw("E1 SAME")

leg = ROOT.TLegend(0.64, 0.57, 1.01, 0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.032)
for pdg, label in ((None, "Total"), (14, "#nu_{#mu}"), (-14, "#bar{#nu}_{#mu}")):
    leg.AddEntry(hist[("cosmic", pdg)], f"Cosmic {label}", "lep")
    leg.AddEntry(hist[("atmo", pdg)], f"Atmospheric {label}", "l")
leg.Draw()

c.Update()
c.SaveAs("plots/atmo_cosmic_reweight.png")

print(f"Diffuse sample: {tree.GetEntries()} saved events, NTot = {ntot:.0f}")
print(f"Energy range: {emin:g} - {emax:g} GeV")
for model, label in (("cosmic", "Cosmic (FUNC1)"), ("atmo", "Atmospheric (Wang-Yasuda)")):
    print(f"{label}: total rate = {hist[(model, None)].Integral():.6e} Hz")
    print(f"  nu_mu = {hist[(model, 14)].Integral():.6e} Hz")
    print(f"  anti-nu_mu = {hist[(model, -14)].Integral():.6e} Hz")

input("Press Enter to exit...")
