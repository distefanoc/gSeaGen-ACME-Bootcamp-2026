#!/usr/bin/env python3
"""Create a widescreen PowerPoint summary from the official exercise plots."""

from pathlib import Path
import sys

try:
    import pptx
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
except ImportError as exc:
    if exc.name and (exc.name == "pptx" or exc.name.startswith("pptx.")):
        print("ERROR: python-pptx is not installed or is incomplete.")
        print("Install it with: python3 -m pip install python-pptx")
    else:
        print(f"ERROR: Missing Python dependency: {exc.name}")
        print("Check your Python installation and required packages.")
    raise SystemExit(1)

print(f"Using python-pptx version {pptx.__version__}")


ROOT = Path(__file__).resolve().parent.parent
PLOTS = ROOT / "plots"
OUTPUT = ROOT / "gseagen_hands_on_results.pptx"

# Each entry is one slide. Exercise 2 has two images on the same slide.
SLIDES = [
    ("Exercise 1 — Diffuse neutrino flux", [
        ("compare_neutrino.png", None),
    ]),
    ("Exercise 2 — Astrophysical neutrino source", [
        ("rxj1713_point.1.png", "Point source"),
        ("rxj1713_extended.1.png", "Extended source"),
    ]),
    ("Exercise 3 — Atmospheric neutrinos: REAL vs WEIGHTED", [
        ("honda_comparison_4plots.png", None),
    ]),
    ("Exercise 4 — Honda vs Wang–Yasuda", [
        ("honda_wang_yasuda.png", None),
    ]),
    ("Exercise 4 — Atmospheric and astrophysical reweighting", [
        ("atmo_cosmic_reweight.png", None),
    ]),
    ("Exercise 5 — Earth transmission: 2D maps", [
        ("pearth_2d.png", None),
    ]),
    ("Exercise 5 — Earth transmission vs energy", [
        ("pearth_vs_energy.png", None),
    ]),
    ("Exercise 5 — Earth transmission vs zenith angle", [
        ("pearth_vs_costheta.png", None),
    ]),
]

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.35)
TITLE_Y = Inches(0.25)
TITLE_H = Inches(0.58)
PLOT_TOP = Inches(1.05)
PLOT_BOTTOM = Inches(7.18)


def add_text(slide, text, left, top, width, height, size, bold=False,
             align=PP_ALIGN.LEFT):
    shape = slide.shapes.add_textbox(left, top, width, height)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(30, 45, 67)


def add_picture_fit(slide, filename, left, top, width, height):
    """Fit an image into a rectangle, preserving its aspect ratio."""
    from PIL import Image

    with Image.open(filename) as image:
        image_w, image_h = image.size
    scale = min(width / image_w, height / image_h)
    picture_w = int(image_w * scale)
    picture_h = int(image_h * scale)
    x = left + (width - picture_w) // 2
    y = top + (height - picture_h) // 2
    slide.shapes.add_picture(str(filename), x, y, width=picture_w,
                             height=picture_h)


def main():
    available = []
    for title, figures in SLIDES:
        found = [(PLOTS / name, label) for name, label in figures
                 if (PLOTS / name).is_file()]
        missing = [name for name, _ in figures
                   if not (PLOTS / name).is_file()]
        for name in missing:
            print(f"Skipping missing plot: plots/{name}")
        if found:
            available.append((title, found))

    if not available:
        print("No official exercise plots found in plots/. No PowerPoint created.")
        return 1

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    cover = prs.slides.add_slide(blank)
    add_text(cover, "gSeaGen — ACME School 2026", Inches(0.85),
             Inches(2.35), Inches(11.65), Inches(0.9), 36, True,
             PP_ALIGN.CENTER)
    add_text(cover, "Hands-on Results", Inches(0.85), Inches(3.45),
             Inches(11.65), Inches(0.65), 26, False, PP_ALIGN.CENTER)

    for title, figures in available:
        slide = prs.slides.add_slide(blank)
        add_text(slide, title, MARGIN, TITLE_Y,
                 SLIDE_W - 2 * MARGIN, TITLE_H, 24, True)
        height = PLOT_BOTTOM - PLOT_TOP
        if len(figures) == 1:
            filename, label = figures[0]
            if label:
                add_text(slide, label, MARGIN, Inches(0.88),
                         SLIDE_W - 2 * MARGIN, Inches(0.3), 16,
                         align=PP_ALIGN.CENTER)
            add_picture_fit(slide, filename, MARGIN, PLOT_TOP,
                            SLIDE_W - 2 * MARGIN, height)
        else:
            gap = Inches(0.3)
            col_w = (SLIDE_W - 2 * MARGIN - gap) // 2
            for index, (filename, label) in enumerate(figures):
                left = MARGIN + index * (col_w + gap)
                add_text(slide, label or "", left, Inches(0.88),
                         col_w, Inches(0.3), 16,
                         align=PP_ALIGN.CENTER)
                add_picture_fit(slide, filename, left, PLOT_TOP,
                                col_w, height)

    prs.save(str(OUTPUT))
    print(f"Created {OUTPUT.name} with {len(prs.slides)} slides "
          f"({sum(len(figures) for _, figures in available)} plots).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
