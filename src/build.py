#!/usr/bin/env python3
"""Assemble the brochure HTML with logos embedded as data URIs."""
import base64, pathlib

here = pathlib.Path(__file__).parent

def uri(name):
    return "data:image/png;base64," + base64.b64encode((here / name).read_bytes()).decode()

html = (here / "brochure.src.html").read_text()
html = html.replace("__AIIMS__", uri("aiims.png"))
html = html.replace("__HTAIN__", uri("htain.png"))
html = html.replace("__QR__", uri("qr.png"))
(here / "brochure.html").write_text(html)
print("wrote brochure.html", len(html), "bytes")
