import ROOT
import os
import math
from atmospheric_flux import atmospheric_numu_flux

ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")
os.makedirs("plots", exist_ok=True)

fhonda = ROOT.TFile.Open("files/honda_weighted.1.et.root")
fdiffuse = ROOT.TFile.Open("files/atmo_cosmic_reweight.1.et.root")
if not fhonda or fhonda.IsZombie() or not fdiffuse or fdiffuse.IsZombie():
    raise RuntimeError("Cannot open one of the input ROOT files")

thonda = fhonda.Get("Events")
tdiffuse = fdiffuse.Get("Events")
if not thonda or not tdiffuse:
    raise RuntimeError("Events tree not found")

def read_ntot(root_file):
    header = root_file.Get("Header")
    if not header or header.GetEntries() == 0:
        raise RuntimeError("Missing Header tree")
    header.GetEntry(0)
    ntot = float(header.Header.NTot)
    if ntot <= 0:
        raise RuntimeError("Invalid NTot")
    return ntot

ntot_honda = read_ntot(fhonda)
ntot_diffuse = read_ntot(fdiffuse)

# Use only the common energy interval of the two samples: 100 GeV - 10 TeV.
emin, emax = 100., 10000.
nbins = 20
species = {None: "total", 14: "numu", -14: "antinumu"}
colors = {None: ROOT.kBlack, 14: ROOT.kRed, -14: ROOT.kGreen + 2}

hist = {}
for sample in ("honda", "wy"):
    for pdg, label in species.items():
        h = ROOT.TH1D(f"h_{sample}_{label}", "", nbins,
                      math.log10(emin), math.log10(emax))
        h.Sumw2()
        h.SetDirectory(0)
        hist[(sample, pdg)] = h

# Honda: EvtWeight already includes the Honda flux.
for entry in thonda:
    event = entry.Events
    nu = event.Tracks[0]
    if nu.E < emin or nu.E > emax or nu.PdgCode not in (14, -14):
        continue
    weight = event.EvtWeight / ntot_honda
    x = math.log10(nu.E)
    hist[("honda", None)].Fill(x, weight)
    hist[("honda", int(nu.PdgCode))].Fill(x, weight)

# Diffuse: GenWeight multiplied by the chosen physical flux.
# Check that the native gSeaGen event class exposes GenWeight.
for entry in tdiffuse:
    event = entry.Events
    nu = event.Tracks[0]
    if nu.E < emin or nu.E > emax or nu.PdgCode not in (14, -14):
        continue
    flux = atmospheric_numu_flux(nu.E, nu.D3, int(nu.PdgCode))
    weight = event.GenWeight / ntot_diffuse * flux
    x = math.log10(nu.E)
    hist[("wy", None)].Fill(x, weight)
    hist[("wy", int(nu.PdgCode))].Fill(x, weight)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

c = ROOT.TCanvas("c_honda_wy", "Honda vs Wang-Yasuda", 1000, 850)
c.Divide(1, 2)

c.cd(1)
ROOT.gPad.SetLeftMargin(0.13)
ROOT.gPad.SetRightMargin(0.05)
ROOT.gPad.SetBottomMargin(0.12)
ROOT.gPad.SetTopMargin(0.06)
ROOT.gPad.SetLogy()

maximum = max(h.GetMaximum() for h in hist.values())
positive = [h.GetBinContent(i) for h in hist.values()
            for i in range(1, nbins + 1) if h.GetBinContent(i) > 0]
minimum = min(positive) if positive else 1e-12

for pdg in species:
    hh = hist[("honda", pdg)]
    hw = hist[("wy", pdg)]
    for h in (hh, hw):
        h.SetLineColor(colors[pdg])
        h.SetMarkerColor(colors[pdg])
        h.SetLineWidth(2)
    hh.SetMarkerStyle(20)
    hh.SetMarkerSize(0.65)
    hw.SetLineStyle(1)

frame = hist[("honda", None)]
frame.SetTitle("Honda vs Wang-Yasuda")
frame.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
frame.GetYaxis().SetTitle("Event rate (Hz / bin)")
frame.GetYaxis().SetTitleOffset(1.4)
frame.SetMinimum(max(minimum * 0.3, 1e-30))
frame.SetMaximum(maximum * 5 if maximum > 0 else 1)
frame.Draw("E1")
for pdg in species:
    hist[("wy", pdg)].Draw("HIST SAME")
for pdg in species:
    hist[("honda", pdg)].Draw("E1 SAME")

leg = ROOT.TLegend(0.57, 0.57, 0.94, 0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.032)
for pdg, label in [(None, "Total"), (14, "#nu_{#mu}"), (-14, "#bar{#nu}_{#mu}")]:
    leg.AddEntry(hist[("honda", pdg)], f"Honda {label}", "lep")
    leg.AddEntry(hist[("wy", pdg)], f"Wang-Yasuda {label}", "l")
leg.Draw()

c.cd(2)
ROOT.gPad.SetLeftMargin(0.13)
ROOT.gPad.SetRightMargin(0.05)
ROOT.gPad.SetBottomMargin(0.16)
ROOT.gPad.SetTopMargin(0.05)

ratios = []
for pdg, label in species.items():
    ratio = hist[("wy", pdg)].Clone(f"ratio_{label}")
    ratio.SetDirectory(0)
    ratio.Divide(hist[("honda", pdg)])
    ratio.SetLineColor(colors[pdg])
    ratio.SetMarkerColor(colors[pdg])
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.65)
    ratio.GetXaxis().SetTitle("log_{10}(E_{#nu}/GeV)")
    ratio.GetYaxis().SetTitle("Wang-Yasuda / Honda")
    ratio.GetYaxis().SetTitleOffset(1.4)
    ratios.append(ratio)

rmax = max((r.GetBinContent(i) + r.GetBinError(i)
            for r in ratios for i in range(1, nbins + 1)
            if r.GetBinContent(i) > 0), default=2.0)
ratios[0].SetMinimum(0)
ratios[0].SetMaximum(max(2., 1.2 * rmax))
ratios[0].Draw("E1")
for r in ratios[1:]:
    r.Draw("E1 SAME")

line = ROOT.TLine(math.log10(emin), 1, math.log10(emax), 1)
line.SetLineStyle(2)
line.Draw("SAME")

c.Update()
c.SaveAs("plots/honda_wang_yasuda.png")

print(f"Honda: {thonda.GetEntries()} saved events, NTot = {ntot_honda:.0f}")
print(f"Diffuse: {tdiffuse.GetEntries()} saved events, NTot = {ntot_diffuse:.0f}")
for sample, label in (("honda", "Honda"), ("wy", "Wang-Yasuda")):
    print(f"{label}: total rate = {hist[(sample, None)].Integral():.6e} Hz")
    print(f"  nu_mu = {hist[(sample, 14)].Integral():.6e} Hz")
    print(f"  anti-nu_mu = {hist[(sample, -14)].Integral():.6e} Hz")
if hist[("honda", None)].Integral() > 0:
    print("Total Wang-Yasuda / Honda = " +
          str(round(hist[("wy", None)].Integral() / hist[("honda", None)].Integral(), 4)))

input("Press Enter to exit...")
