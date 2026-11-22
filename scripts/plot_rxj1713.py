
import ROOT
import ctypes
import math
from array import array
import argparse
import os



parser = argparse.ArgumentParser(
    description="Plot equatorial coordinates of neutrinos from RX J1713.7-3946"
)

parser.add_argument(
    "input_file",
    help="Input gSeaGen ROOT file"
)

args = parser.parse_args()

ROOT.gSystem.Load("libGSeaEvent")
ROOT.gSystem.Load("libGSeaNuDrivers")
ROOT.gInterpreter.Declare('#include "SeaEvent/GSeaEvent.h"')
ROOT.gInterpreter.Declare('#include "SeaNuDrivers/GAstro.h"')

# Detector coordinates (radians)
astro = ROOT.GAstro(0.632973, 0.280998)

# Source coordinates (J2000)
ra0_deg = 258.39
dec0_deg = -39.76

ra_source = ra0_deg / 15.0  # hours
dec_source = dec0_deg       # degrees


def direction_to_equatorial(event):
    """Convert neutrino direction to equatorial coordinates at event epoch."""

    nu = event.Neutrino

    az = ctypes.c_double()
    alt = ctypes.c_double()
    ra = ctypes.c_double()
    dec = ctypes.c_double()

    # Reverse neutrino propagation direction
    astro.Direction2Hor(-nu.D1, -nu.D2, -nu.D3, az, alt)

    # Horizontal -> equatorial coordinates
    astro.Hor2Eq(alt.value, az.value, event.LST, ra, dec)

    return math.degrees(ra.value) / 15.0, math.degrees(dec.value)


def source_coordinates_at_mjd(mjd):
    """Apply precession and nutation to the J2000 source coordinates."""

    ra_prec = ctypes.c_double()
    dec_prec = ctypes.c_double()

    astro.CalcPrecession(
        51544.5, mjd,
        math.radians(ra0_deg), math.radians(dec0_deg),
        ra_prec, dec_prec
    )

    ra_nut = ctypes.c_double()
    dec_nut = ctypes.c_double()

    astro.CalcNutation(
        mjd, ra_prec.value, dec_prec.value,
        ra_nut, dec_nut
    )

    return math.degrees(ra_nut.value) / 15.0, math.degrees(dec_nut.value)


# Source position at 1 January 2021, 00:00 UTC
ra_2021, dec_2021 = source_coordinates_at_mjd(59215.0)

print("Source J2000:")
print("  RA =", ra_source, "hours")
print("  Dec =", dec_source, "degrees")

print("Source 1 January 2021:")
print("  RA =", ra_2021, "hours")
print("  Dec =", dec_2021, "degrees")


# Read generated events
f = ROOT.TFile.Open(args.input_file)

if not f or f.IsZombie():
    raise RuntimeError("Cannot open ROOT file")

tree = f.Get("Events")

ra_values = array("d")
dec_values = array("d")

for entry in tree:
    event = entry.Events
    ra, dec = direction_to_equatorial(event)

    ra_values.append(ra)
    dec_values.append(dec)

print("Number of events:", len(ra_values))
print("RA range:", min(ra_values), max(ra_values))
print("Dec range:", min(dec_values), max(dec_values))


# Plot ranges
ra_min, ra_max = 17.15, 17.32
dec_min, dec_max = -40.55, -38.95

# Angular extent of the RA axis, accounting for declination
ra_span_deg = (ra_max - ra_min) * 15.0 * math.cos(math.radians(dec0_deg))
dec_span_deg = dec_max - dec_min

# Canvas margins
left_margin = 0.14
right_margin = 0.05
bottom_margin = 0.12
top_margin = 0.08

# Desired canvas dimensions
canvas_width = 850

# Compute height for equal angular scales
plot_width = canvas_width * (1.0 - left_margin - right_margin)
plot_height = plot_width * dec_span_deg / ra_span_deg
canvas_height = round(plot_height / (1.0 - bottom_margin - top_margin))

# Create canvas
canvas = ROOT.TCanvas("canvas", "RX J1713.7-3946", 850, 750)

# Set the actual canvas drawing dimensions
canvas.SetCanvasSize(canvas_width, canvas_height)

canvas.SetLeftMargin(left_margin)
canvas.SetRightMargin(right_margin)
canvas.SetBottomMargin(bottom_margin)
canvas.SetTopMargin(top_margin)

print("Canvas size:", canvas_width, canvas_height)


# Neutrino directions
graph = ROOT.TGraph(len(ra_values), ra_values, dec_values)

graph.SetTitle("RX J1713.7-3946;RA (hour);#delta (deg)")
graph.SetMarkerStyle(6)
graph.SetMarkerColor(ROOT.kBlack)

graph.Draw("AP")

graph.GetXaxis().SetLimits(ra_min, ra_max)
graph.SetMinimum(dec_min)
graph.SetMaximum(dec_max)


# Source position in J2000: red star
star = ROOT.TMarker(ra_source, dec_source, 29)
star.SetMarkerColor(ROOT.kRed)
star.SetMarkerSize(2.0)
star.Draw()


# Source position at 1 January 2021
# White outline for contrast against neutrino points
marker_2021_bg = ROOT.TEllipse(
    ra_2021, dec_2021, 0.003, 0.035
)
marker_2021_bg.SetFillStyle(0)
marker_2021_bg.SetLineColor(ROOT.kWhite)
marker_2021_bg.SetLineWidth(8)
marker_2021_bg.Draw()

# Green outline
marker_2021 = ROOT.TEllipse(
    ra_2021, dec_2021, 0.003, 0.035
)
marker_2021.SetFillStyle(0)
marker_2021.SetLineColor(ROOT.kGreen + 2)
marker_2021.SetLineWidth(4)
marker_2021.Draw()


# Legend
legend = ROOT.TLegend(0.16, 0.80, 0.49, 0.90)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

# Open-circle symbol for the legend
legend_marker = ROOT.TMarker(0, 0, 24)
legend_marker.SetMarkerColor(ROOT.kGreen + 2)
legend_marker.SetMarkerSize(2.0)

legend.AddEntry(star, "Source (J2000)", "p")
legend.AddEntry(legend_marker, "Source (1 Jan 2021)", "p")
legend.Draw()


# Save plot
canvas.Modified()
canvas.Update()
output_file = os.path.splitext(args.input_file)[0]

if output_file.endswith(".et"):
    output_file = output_file[:-3]

output_file += ".png"

canvas.SaveAs(output_file)
f.Close()

input("Press Enter to close the plot...")
