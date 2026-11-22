import ROOT
import os
import argparse
import math

# Compare the weighted neutrino distributions from the 1-bin and 5-bin runs.
ROOT.gSystem.Load(os.environ["GSEAGEN"] + "/lib/libGSeaEvent.so")

parser = argparse.ArgumentParser(
    description="Compare weighted neutrino distributions from two gSeaGen simulations"
)
parser.add_argument("one_bin_file", help="ROOT file generated with 1 energy bin")
parser.add_argument("five_bin_file", help="ROOT file generated with 5 energy bins")
args = parser.parse_args()

nbin = 25
seconds_per_year = 365.25 * 86400


def read_sample(filename, label, suffix):
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        raise RuntimeError("Cannot open " + filename)

    header = f.Get("Header")
    tree = f.Get("Events")
    if not header or not tree:
        raise RuntimeError("Missing Header or Events tree in " + filename)

    header.GetEntry(0)
    gp = header.Header
    ntot = gp.NTot
    emin, emax = gp.EvMin, gp.EvMax
    ctmin, ctmax = gp.CtMin, gp.CtMax

    # Keep the same physical normalisation and binning as plot_neutrino.py.
    hE = ROOT.TH1D("hE_" + suffix, label, nbin,
                   math.log10(emin), math.log10(emax))
    hCt = ROOT.TH1D("hCt_" + suffix, label, nbin, ctmin, ctmax)
    hE.SetDirectory(0)
    hCt.SetDirectory(0)
    hE.Sumw2()
    hCt.Sumw2()

    for entry in tree:
        event = entry.Events
        nu = event.Tracks[0]
        weight = event.EvtWeight / ntot
        hE.Fill(math.log10(nu.E), weight)
        hCt.Fill(nu.D3, weight)

    return {
        "file": f, "label": label, "hE": hE, "hCt": hCt,
        "range": (emin, emax, ctmin, ctmax),
        "saved": tree.GetEntries(), "rate": hE.Integral(),
    }


one = read_sample(args.one_bin_file, "1 energy bin", "one")
five = read_sample(args.five_bin_file, "5 energy bins", "five")

if any(not math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
       for a, b in zip(one["range"], five["range"])):
    raise ValueError("The two simulations have different energy or angular ranges.")

ROOT.gStyle.SetOptStat(0)

for sample, color, marker in ((one, ROOT.kBlue, 20),
                              (five, ROOT.kRed, 24)):
    for hist in (sample["hE"], sample["hCt"]):
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
        hist.SetMarkerStyle(marker)
        hist.SetMarkerSize(0.8)
        hist.SetLineWidth(2)


def draw_comparison(pad, key, title, xlabel):
    h1, h5 = one[key], five[key]
    pad.SetLeftMargin(0.16)  # Same Y-axis margin as plot_neutrino.py.
    pad.SetRightMargin(0.05)
    pad.SetBottomMargin(0.12)
    pad.cd()

    # Use the same Y scale and show statistical uncertainties on both samples.
    ymax = max(h1.GetMaximum(), h5.GetMaximum())
    h1.SetMaximum(ymax * 1.35)
    h1.SetMinimum(0.0)
    h1.SetTitle(title)
    h1.GetXaxis().SetTitle(xlabel)
    h1.GetYaxis().SetTitle("Event rate (Hz)")
    h1.Draw("E1")
    h5.Draw("E1 SAME")

    legend = ROOT.TLegend(0.60, 0.76, 0.91, 0.89)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(h1, "1 energy bin", "lep")
    legend.AddEntry(h5, "5 energy bins", "lep")
    legend.Draw()
    return legend


os.makedirs("plots", exist_ok=True)
canvas = ROOT.TCanvas("cCompare", "Weighted neutrino distributions", 1200, 500)
canvas.Divide(2, 1)

legendE = draw_comparison(
    canvas.cd(1), "hE", "Weighted neutrino energy",
    "log_{10}(E_{#nu}/GeV)")
legendCt = draw_comparison(
    canvas.cd(2), "hCt", "Weighted neutrino zenith angle",
    "cos#theta_{#nu}")

canvas.Update()
canvas.SaveAs("plots/compare_neutrino.png")

rate1, rate5 = one["rate"], five["rate"]
saved1, saved5 = one["saved"], five["saved"]

print("\nComparison of 1-bin and 5-bin simulations")
print("\nUNWEIGHTED (MC statistics: saved event counts)")
print(f"  1 energy bin:                  {saved1} events")
print(f"  5 energy bins:                 {saved5} events")
if saved1 != 0:
    print(f"  Saved events ratio (5 / 1):    {saved5 / saved1:.2f}")
else:
    print("  Saved events ratio (5 / 1):    undefined (zero events)")

print("\nWEIGHTED (Physical event rates)")
print(f"  1 energy bin:                  {rate1:.4e} Hz  ({rate1 * seconds_per_year:.2f} events/year)")
print(f"  5 energy bins:                 {rate5:.4e} Hz  ({rate5 * seconds_per_year:.2f} events/year)")
if rate1 != 0:
    ratio = rate5 / rate1
    print(f"  Event rate ratio (5 / 1):      {ratio:.4f}")
    print(f"  Relative rate difference:     {(ratio - 1) * 100:+.2f}%")
else:
    print("  Event rate ratio (5 / 1):      undefined (zero rate)")

input("Press Enter to close the plot...")
