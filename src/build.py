#!/usr/bin/env python3
"""Assemble the brochure and agenda HTML with logos embedded as data URIs."""
import base64, pathlib

here = pathlib.Path(__file__).parent

def uri(name):
    return "data:image/png;base64," + base64.b64encode((here / name).read_bytes()).decode()

def assemble(name, out):
    html = (here / name).read_text()
    for key, png in (("__AIIMS__", "aiims.png"), ("__HTAIN__", "htain.png"), ("__QR__", "qr.png")):
        html = html.replace(key, uri(png))
    out.write_text(html)
    print("wrote", out.name, len(html), "bytes")

assemble("brochure.src.html", here.parent / "brochure.html")
assemble("agenda.src.html", here.parent / "agenda.html")
