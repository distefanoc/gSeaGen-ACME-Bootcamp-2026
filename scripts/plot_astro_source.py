import argparse
import ctypes
import math
import os
from array import array
from datetime import datetime, timezone

import ROOT

parser = argparse.ArgumentParser(
    description="Plot equatorial neutrino directions for a gSeaGen astrophysical source"
)
parser.add_argument("input_file", help="Input gSeaGen ROOT file")
args = parser.parse_args()

ROOT.gSystem.Load("libGSeaEvent")
ROOT.gSystem.Load("libGSeaNuDrivers")
ROOT.gInterpreter.Declare('#include "SeaEvent/GSeaEvent.h"')
ROOT.gInterpreter.Declare('#include "SeaNuDrivers/GAstro.h"')

f = ROOT.TFile.Open(args.input_file)
if not f or f.IsZombie():
    raise RuntimeError(f"Cannot open ROOT file: {args.input_file}")

header_tree = f.Get("Header")
if not header_tree or header_tree.GetEntries() == 0:
    raise RuntimeError("Cannot find a populated Header tree")
header_tree.GetEntry(0)
gp = header_tree.Header

if str(gp.GenMode).upper() != "POINT":
    raise RuntimeError(f"Expected POINT generation mode, got {gp.GenMode}")

# Detector coordinates are stored in radians.
astro = ROOT.GAstro(gp.SiteLatitude, gp.SiteLongitude)

# Assume the source coordinates in GenParam are J2000, stored in radians.
source_name = str(gp.SourceName) or "Astrophysical source"
ra0_deg = math.degrees(gp.RightAscension)
dec0_deg = math.degrees(gp.Declination)
source_radius_deg = math.degrees(gp.SourceRadius)
ra_source = ra0_deg / 15.0

mjd_start = float(gp.MJDStart)
if mjd_start <= 0:
    raise RuntimeError("Invalid MJDStart in header")

# Use the first instant of the generation interval for the reference marker.
if gp.TimeStampStart:
    date_start = datetime.fromtimestamp(int(gp.TimeStampStart), tz=timezone.utc)
else:
    date_start = datetime.fromtimestamp((mjd_start - 40587.0) * 86400, tz=timezone.utc)
date_label = date_start.strftime("%d %b %Y")

print(f"Source: {source_name}")
print(f"Generation mode: {gp.GenMode}")
print(f"RA (assumed J2000):  {ra0_deg:.4f} deg")
print(f"Dec (assumed J2000): {dec0_deg:.4f} deg")
print(f"Source radius: {source_radius_deg:.4f} deg")
print(f"Site latitude: {gp.SiteLatitude:.6f} rad")
print(f"Site longitude: {gp.SiteLongitude:.6f} rad")
print(f"Start MJD: {mjd_start:.6f} ({date_label} UTC)")


def direction_to_equatorial(event):
    """Convert neutrino propagation direction to source direction at event epoch."""
    nu = event.Neutrino
    az, alt = ctypes.c_double(), ctypes.c_double()
    ra, dec = ctypes.c_double(), ctypes.c_double()

    # Reverse the propagation direction to point towards the source.
    astro.Direction2Hor(-nu.D1, -nu.D2, -nu.D3, az, alt)
    astro.Hor2Eq(alt.value, az.value, event.LST, ra, dec)
    return math.degrees(ra.value) / 15.0, math.degrees(dec.value)


def source_coordinates_at_mjd(mjd):
    """Apply gSeaGen's precession and nutation corrections from J2000."""
    ra_prec, dec_prec = ctypes.c_double(), ctypes.c_double()
    astro.CalcPrecession(
        51544.5, mjd,
        math.radians(ra0_deg), math.radians(dec0_deg),
        ra_prec, dec_prec,
    )
    ra_nut, dec_nut = ctypes.c_double(), ctypes.c_double()
    astro.CalcNutation(mjd, ra_prec.value, dec_prec.value, ra_nut, dec_nut)
    return math.degrees(ra_nut.value) / 15.0, math.degrees(dec_nut.value)


ra_start, dec_start = source_coordinates_at_mjd(mjd_start)
print(f"Source at {date_label}: RA = {ra_start:.6f} h, Dec = {dec_start:.6f} deg")

tree = f.Get("Events")
if not tree:
    raise RuntimeError("Cannot find Events tree")

ra_values, dec_values = array("d"), array("d")
for entry in tree:
    ra, dec = direction_to_equatorial(entry.Events)
    ra_values.append(ra)
    dec_values.append(dec)

if not ra_values:
    raise RuntimeError("No events found")

print("Number of events:", len(ra_values))
print("RA range:", min(ra_values), max(ra_values))
print("Dec range:", min(dec_values), max(dec_values))

# Center the plot on the source; include all events and both reference positions.
# Unwrap RA around the source to avoid discontinuities at 0/24 hours.
def unwrap_ra(ra):
    return ra_source + (ra - ra_source + 12.0) % 24.0 - 12.0

ra_values = array("d", (unwrap_ra(ra) for ra in ra_values))
ra_start = unwrap_ra(ra_start)

ra_all = list(ra_values) + [ra_source, ra_start]
dec_all = list(dec_values) + [dec0_deg, dec_start]


# Plot a field of at least 1 degree around the source
plot_radius = max(1.0, source_radius_deg)

dec_min = dec_start - plot_radius
dec_max = dec_start + plot_radius

# Account for the convergence of right ascension at the source declination
ra_half_width = plot_radius / (
    15.0 * math.cos(math.radians(dec_start))
)

ra_min = ra_start - ra_half_width
ra_max = ra_start + ra_half_width


# Correct the aspect ratio for RA (hours) and cos(declination).
ra_span_deg = (ra_max - ra_min) * 15.0 * max(abs(math.cos(math.radians(dec0_deg))), 0.01)
dec_span_deg = dec_max - dec_min
left_margin, right_margin = 0.14, 0.05
bottom_margin, top_margin = 0.12, 0.08
canvas_width = 700
plot_width = canvas_width * (1.0 - left_margin - right_margin)
plot_height = plot_width * dec_span_deg / ra_span_deg
canvas_height = max(400, round(plot_height / (1.0 - bottom_margin - top_margin)))

canvas = ROOT.TCanvas("canvas", source_name, canvas_width, canvas_height)
canvas.SetLeftMargin(left_margin)
canvas.SetRightMargin(right_margin)
canvas.SetBottomMargin(bottom_margin)
canvas.SetTopMargin(top_margin)
print("Canvas size:", canvas_width, canvas_height)

graph = ROOT.TGraph(len(ra_values), ra_values, dec_values)
graph.SetTitle(f"{source_name};RA (hour);#delta (deg)")
graph.SetMarkerStyle(6)
graph.SetMarkerColor(ROOT.kBlack)
graph.Draw("AP")
graph.GetXaxis().SetLimits(ra_min, ra_max)
graph.SetMinimum(dec_min)
graph.SetMaximum(dec_max)

# J2000 source position: red star.
star = ROOT.TMarker(ra_source, dec0_deg, 29)
star.SetMarkerColor(ROOT.kRed)
star.SetMarkerSize(2.0)
star.Draw()

# Position at the start of generation: white halo and green outline.
# Scale the ellipse to preserve the original marker's visual proportions.
ellipse_ra = 0.003
ellipse_dec = 0.035
marker_bg = ROOT.TEllipse(ra_start, dec_start, ellipse_ra, ellipse_dec)
marker_bg.SetFillStyle(0)
marker_bg.SetLineColor(ROOT.kWhite)
marker_bg.SetLineWidth(8)
marker_bg.Draw()

marker_start = ROOT.TEllipse(ra_start, dec_start, ellipse_ra, ellipse_dec)
marker_start.SetFillStyle(0)
marker_start.SetLineColor(ROOT.kGreen + 2)
marker_start.SetLineWidth(4)
marker_start.Draw()

legend = ROOT.TLegend(0.16, 0.80, 0.49, 0.90)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend_marker = ROOT.TMarker(0, 0, 24)
legend_marker.SetMarkerColor(ROOT.kGreen + 2)
legend_marker.SetMarkerSize(2.0)
legend.AddEntry(star, "Source (J2000)", "p")
legend.AddEntry(legend_marker, f"Source ({date_label})", "p")
legend.Draw()

canvas.Modified()
canvas.Update()
os.makedirs("plots", exist_ok=True)
name = os.path.basename(args.input_file)
name = name[:-8] if name.endswith(".et.root") else os.path.splitext(name)[0]
output_file = os.path.join("plots", name + ".png")
canvas.SaveAs(output_file)
print("Saved plot:", output_file)
f.Close()

input("Press Enter to close the plot...")
