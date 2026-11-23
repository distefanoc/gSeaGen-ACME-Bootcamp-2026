"""Local test: plot gSeaGen source neutrino directions in J2000 coordinates.

Uses GAstro for all available transformations. The inverse nutation is
implemented iteratively, inverting GAstro's own first-order formulas.
"""
import argparse
import ctypes
import math
import os
from array import array

import ROOT

J2000_MJD = 51544.5
TWO_PI = 2.0 * math.pi


def angular_difference(a, b):
    return (a - b + math.pi) % TWO_PI - math.pi


def inverse_nutation(astro, mjd, ra_apparent, dec_apparent, tolerance=1e-13):
    """Invert GAstro.CalcNutation by fixed-point iteration (angles in radians)."""
    ra_mean, dec_mean = ra_apparent, dec_apparent
    for iteration in range(20):
        ra_out, dec_out = ctypes.c_double(), ctypes.c_double()
        astro.CalcNutation(mjd, ra_mean, dec_mean, ra_out, dec_out)
        dra = angular_difference(ra_apparent, ra_out.value)
        ddec = dec_apparent - dec_out.value
        ra_mean = (ra_mean + dra) % TWO_PI
        dec_mean += ddec
        if max(abs(dra), abs(ddec)) < tolerance:
            return ra_mean, dec_mean
    raise RuntimeError(f"Inverse nutation did not converge at MJD {mjd}")


def inverse_precession(astro, mjd, ra_mean, dec_mean):
    """Invert Meeus precession using the same GAstro routine with epochs swapped."""
    ra, dec = ctypes.c_double(), ctypes.c_double()
    astro.CalcPrecession(mjd, J2000_MJD, ra_mean, dec_mean, ra, dec)
    return ra.value % TWO_PI, dec.value


def apparent_to_j2000(astro, mjd, ra, dec):
    ra_mean, dec_mean = inverse_nutation(astro, mjd, ra, dec)
    return inverse_precession(astro, mjd, ra_mean, dec_mean)


def j2000_to_apparent(astro, mjd, ra, dec):
    ra_p, dec_p = ctypes.c_double(), ctypes.c_double()
    astro.CalcPrecession(J2000_MJD, mjd, ra, dec, ra_p, dec_p)
    ra_a, dec_a = ctypes.c_double(), ctypes.c_double()
    astro.CalcNutation(mjd, ra_p.value, dec_p.value, ra_a, dec_a)
    return ra_a.value, dec_a.value


def event_mjd(event, astro):
    """Read event epoch; fail explicitly rather than substituting generation start."""
    for field in ("MJD", "EventMJD", "Mjd"):
        if hasattr(event, field):
            value = float(getattr(event, field))
            if value > 40000:
                return value
    for sec_name, tick_name in (
        ("TimeStampSec", "TimeStampTick"),
        ("TimestampSec", "TimestampTick"),
        ("TimeStamp", "TimeStampTick"),
    ):
        if hasattr(event, sec_name):
            sec = int(getattr(event, sec_name))
            tick = int(getattr(event, tick_name)) if hasattr(event, tick_name) else 0
            if sec > 0:
                return float(astro.CalcMJDFromTimeStamp(sec, tick))
    available = [name for name in dir(event) if "time" in name.lower() or "mjd" in name.lower()]
    raise RuntimeError(
        "Cannot determine the MJD of this event. "
        f"Available time-related fields: {available}. "
        "Please inspect GSeaEvent.h; MJDStart is not a valid substitute."
    )


def separation_arcsec(ra1, dec1, ra2, dec2):
    dra = angular_difference(ra1, ra2)
    x = math.cos(dec1) * math.cos(dec2) * math.cos(dra) + math.sin(dec1) * math.sin(dec2)
    return math.degrees(math.acos(max(-1.0, min(1.0, x)))) * 3600.0


def main():
    parser = argparse.ArgumentParser(description="Plot gSeaGen neutrino directions in J2000")
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

    astro = ROOT.GAstro(gp.SiteLatitude, gp.SiteLongitude)
    source_name = str(gp.SourceName) or "Astrophysical source"
    ra0, dec0 = float(gp.RightAscension), float(gp.Declination)
    source_radius_deg = math.degrees(float(gp.SourceRadius))
    mjd_start = float(gp.MJDStart)
    if mjd_start <= 0:
        raise RuntimeError("Invalid MJDStart in header")

    print(f"Source: {source_name}")
    print(f"J2000: RA={math.degrees(ra0)/15:.6f} h, Dec={math.degrees(dec0):.6f} deg")
    print(f"Radius: {source_radius_deg:.4f} deg")
    print(f"Start MJD: {mjd_start:.6f}")

    # Check inverse consistency using GAstro's forward calculation.
    mjd_samples = [mjd_start]
    if hasattr(gp, "MJDEnd") and float(gp.MJDEnd) > mjd_start:
        mjd_samples.extend([(mjd_start + float(gp.MJDEnd))/2, float(gp.MJDEnd)])
    for mjd in mjd_samples:
        ra_app, dec_app = j2000_to_apparent(astro, mjd, ra0, dec0)
        ra_back, dec_back = apparent_to_j2000(astro, mjd, ra_app, dec_app)
        # Compare component differences to avoid acos precision loss at tiny angles.
        residual = math.hypot(angular_difference(ra_back, ra0)*math.cos(dec0), dec_back-dec0)
        print(f"Round-trip MJD {mjd:.6f}: {math.degrees(residual)*3600:.6g} arcsec")
        if residual > 1e-7:
            raise RuntimeError("Precession/nutation round-trip exceeds tolerance")

    tree = f.Get("Events")
    if not tree:
        raise RuntimeError("Cannot find Events tree")
    ra_values, dec_values = array("d"), array("d")
    event_times = []
    for entry in tree:
        event = entry.Events
        mjd = event_mjd(event, astro)
        event_times.append(mjd)
        nu = event.Neutrino
        az, alt = ctypes.c_double(), ctypes.c_double()
        ra_epoch, dec_epoch = ctypes.c_double(), ctypes.c_double()
        # Reverse propagation vector to obtain incoming source direction.
        astro.Direction2Hor(-nu.D1, -nu.D2, -nu.D3, az, alt)
        astro.Hor2Eq(alt.value, az.value, event.LST, ra_epoch, dec_epoch)
        ra_j2000, dec_j2000 = apparent_to_j2000(astro, mjd, ra_epoch.value, dec_epoch.value)
        ra_values.append(math.degrees(ra_j2000)/15.0)
        dec_values.append(math.degrees(dec_j2000))

    if not ra_values:
        raise RuntimeError("No events found")
    print(f"Events: {len(ra_values)}, MJD range: {min(event_times):.6f}–{max(event_times):.6f}")

    ra_source = math.degrees(ra0)/15.0
    dec_source = math.degrees(dec0)
    ra_values = array("d", (ra_source + (ra-ra_source+12.0)%24.0-12.0 for ra in ra_values))

    # Use a common angular field centered on the J2000 source position.
    plot_radius = max(1.0, source_radius_deg)
    cos_dec = max(abs(math.cos(dec0)), 0.01)
    ra_half_width = plot_radius/(15.0*cos_dec)
    ra_min, ra_max = ra_source-ra_half_width, ra_source+ra_half_width
    dec_min, dec_max = dec_source-plot_radius, dec_source+plot_radius

    left_margin, right_margin = 0.14, 0.05
    bottom_margin, top_margin = 0.12, 0.08
    canvas_width = 600
    plot_width = canvas_width*(1-left_margin-right_margin)
    ra_span_deg = (ra_max-ra_min)*15*cos_dec
    plot_height = plot_width*(dec_max-dec_min)/ra_span_deg
    canvas_height = max(400, round(plot_height/(1-bottom_margin-top_margin)) + 22)
    canvas = ROOT.TCanvas("canvas", source_name, canvas_width, canvas_height)
    canvas.SetLeftMargin(left_margin)
    canvas.SetRightMargin(right_margin)
    canvas.SetBottomMargin(bottom_margin)
    canvas.SetTopMargin(top_margin)

    graph = ROOT.TGraph(len(ra_values), ra_values, dec_values)
    graph.SetTitle(f"{source_name} (J2000);RA (hour);#delta (deg)")
    graph.SetMarkerStyle(6)
    graph.SetMarkerColor(ROOT.kBlack)
    graph.Draw("AP")
    graph.GetXaxis().SetLimits(ra_min, ra_max)
    graph.SetMinimum(dec_min)
    graph.SetMaximum(dec_max)

    # Open circle instead of a filled star, so point-source events remain visible.
    # Keep the same ellipse dimensions used for the 2021 marker in the old script.
    marker_bg = ROOT.TEllipse(ra_source, dec_source, 0.003, 0.035)
    marker_bg.SetFillStyle(0)
    marker_bg.SetLineColor(ROOT.kWhite)
    marker_bg.SetLineWidth(8)
    marker_bg.Draw()

    marker_source = ROOT.TEllipse(ra_source, dec_source, 0.003, 0.035)
    marker_source.SetFillStyle(0)
    marker_source.SetLineColor(ROOT.kRed)
    marker_source.SetLineWidth(4)
    marker_source.Draw()

    legend = ROOT.TLegend(0.16, 0.83, 0.48, 0.90)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend_marker = ROOT.TMarker(0, 0, 24)
    legend_marker.SetMarkerColor(ROOT.kRed)
    legend_marker.SetMarkerSize(2.0)
    legend.AddEntry(legend_marker, "Source (J2000)", "p")
    legend.Draw()
    canvas.Modified()
    canvas.Update()
    
    os.makedirs("plots", exist_ok=True)
    name = os.path.basename(args.input_file)
    name = name[:-8] if name.endswith(".et.root") else os.path.splitext(name)[0]
    output_file = os.path.join("plots", name+".png")
    canvas.SaveAs(output_file)
    print("Saved plot:", output_file)
    f.Close()
    input("Press Enter to close the plot...")


if __name__ == "__main__":
    main()
