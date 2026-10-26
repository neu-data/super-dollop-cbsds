"""Compile the course diagrams, crop them to their content and render PNGs.

Run from this folder:  python build_diagrams.py [name ...]
Needs pdflatex (TinyTeX or any TeX distribution) and PyMuPDF (pip install pymupdf).
Decision diagrams (D*) are written next to their .tex source; the two causal
diagrams (dag_*) are also copied as PNG to ../../figures/ for slides and workbook.
"""
import os
import shutil
import subprocess
import sys

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES = os.path.normpath(os.path.join(HERE, "..", "..", "figures"))
DPI = 200
MARGIN_PT = 12


def content_rect(page):
    """Bounding box of non-white pixels, in PDF points."""
    zoom = 1.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    w, h, n = pix.width, pix.height, pix.n
    data = pix.samples
    rows = [y for y in range(h) if any(data[(y * w + x) * n] < 250 for x in range(0, w, 2))]
    cols = [x for x in range(w) if any(data[(y * w + x) * n] < 250 for y in range(rows[0], rows[-1] + 1, 2))]
    r = fitz.Rect(cols[0], rows[0], cols[-1] + 1, rows[-1] + 1) / zoom
    return (r + (-MARGIN_PT, -MARGIN_PT, MARGIN_PT, MARGIN_PT)) & page.rect


def build(name):
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"],
                   cwd=HERE, check=True, stdout=subprocess.DEVNULL)
    for ext in (".aux", ".log"):
        p = os.path.join(HERE, name + ext)
        if os.path.exists(p):
            os.remove(p)
    pdf = os.path.join(HERE, name + ".pdf")
    doc = fitz.open(pdf)
    page = doc[0]
    page.set_cropbox(content_rect(page))
    tmp = pdf + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, pdf)
    doc = fitz.open(pdf)
    png = os.path.join(HERE, name + ".png")
    doc[0].get_pixmap(dpi=DPI, alpha=False).save(png)
    doc.close()
    if name.startswith("dag_"):
        os.makedirs(FIGURES, exist_ok=True)
        shutil.copy(png, os.path.join(FIGURES, name + ".png"))
    print("built", name)


if __name__ == "__main__":
    names = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(HERE)
                                   if f.endswith(".tex") and f != "diagram_style.tex")
    for nm in names:
        build(nm)
