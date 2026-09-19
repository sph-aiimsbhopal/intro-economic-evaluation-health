#!/usr/bin/env python3
"""Recolour the brochure and agenda by swapping the :root custom-property block.

Usage:  python3 palettes.py <name>        # apply a palette to the two .src.html files
        python3 palettes.py --list
Everything visual routes through these variables, so nothing else needs touching.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent

PALETTES = {
    # ---------------------------------------------------------------- teal (the R-workshop scheme)
    "teal": {
        "deep": "#16414e", "deep-2": "#12586a", "bar": "#123845",
        "teal": "#0d7f8c", "teal-br": "#12a3a8",
        "green": "#4aa87b", "amber": "#d9a227",
        "mint": "#eaf5f4", "mint-br": "#cfe6e4", "line": "#dde5e8",
        "ink": "#22333b", "ink-2": "#4a5c66", "ink-3": "#7b8c95", "ink-body": "#2d3f47",
        "on-1": "#bfe6e6", "on-2": "#9fd2d4", "on-3": "#8dc3c8", "on-4": "#d6ecee", "on-5": "#b9d2d8",
        "icon": "#5fc9cf", "link": "#7fd4d8",
        "tint": "#f4f8f8", "tint-2": "#fafcfc", "tint-3": "#f6f9f9",
        "rule-mid": "#3fb489", "reg-1": "#0e7f88", "reg-2": "#14a08c",
        "slot-b": "#a9781a", "slot-c": "#2f7d59",
        "note-bg": "#fdf6e3", "note-br": "#f0e0b0", "note-ink": "#5c4a1c", "note-b": "#7a5e12",
    },
    # ---------------------------------------------------------------- A. indigo and gold
    "indigo": {
        "deep": "#1c2f5e", "deep-2": "#2c4a8f", "bar": "#16264d",
        "teal": "#2a4890", "teal-br": "#c08e2a",
        "green": "#3d8a63", "amber": "#c08e2a",
        "mint": "#eef2fa", "mint-br": "#d5deef", "line": "#dee3ec",
        "ink": "#22283b", "ink-2": "#4c5670", "ink-3": "#7d8699", "ink-body": "#2c3448",
        "on-1": "#cdd9f2", "on-2": "#aab9de", "on-3": "#9fb2dd", "on-4": "#dde5f5", "on-5": "#c0cbe2",
        "icon": "#8fa6dd", "link": "#a9bdea",
        "tint": "#f4f6fb", "tint-2": "#fbfcfe", "tint-3": "#f6f8fc",
        "rule-mid": "#6f7fbe", "reg-1": "#23397a", "reg-2": "#3a5cae",
        "slot-b": "#a9781a", "slot-c": "#2f7d59",
        "note-bg": "#fdf6e3", "note-br": "#f0e0b0", "note-ink": "#5c4a1c", "note-b": "#7a5e12",
    },
    # ---------------------------------------------------------------- B. maroon and terracotta
    "maroon": {
        "deep": "#5c1d26", "deep-2": "#82333a", "bar": "#47161d",
        "teal": "#8c2f33", "teal-br": "#c2603f",
        "green": "#4a7d5a", "amber": "#c08e2a",
        "mint": "#fbf1ee", "mint-br": "#eed9d1", "line": "#e6dcd9",
        "ink": "#2e2326", "ink-2": "#5e4e50", "ink-3": "#8f7f80", "ink-body": "#3a2c2e",
        "on-1": "#f0cfc7", "on-2": "#dfb2a8", "on-3": "#d8a99f", "on-4": "#f7e5e0", "on-5": "#e0c3bc",
        "icon": "#e0a08c", "link": "#eab5a0",
        "tint": "#faf5f3", "tint-2": "#fdfbfa", "tint-3": "#faf6f4",
        "rule-mid": "#b0503f", "reg-1": "#7a2b31", "reg-2": "#a8523f",
        "slot-b": "#a9781a", "slot-c": "#4a7d5a",
        "note-bg": "#f7f1e6", "note-br": "#e8dcc4", "note-ink": "#5c4a1c", "note-b": "#7a5e12",
    },
    # ---------------------------------------------------------------- C. charcoal and saffron
    "charcoal": {
        "deep": "#232830", "deep-2": "#3a424e", "bar": "#1b1f26",
        "teal": "#414a57", "teal-br": "#d1860f",
        "green": "#4a8560", "amber": "#d1860f",
        "mint": "#f3f4f6", "mint-br": "#dfe2e7", "line": "#e0e3e7",
        "ink": "#23272d", "ink-2": "#4e555e", "ink-3": "#7f8790", "ink-body": "#2c3138",
        "on-1": "#cfd5de", "on-2": "#aab2be", "on-3": "#a5adba", "on-4": "#e2e6eb", "on-5": "#bcc3cd",
        "icon": "#e0a03c", "link": "#e8b45c",
        "tint": "#f5f6f7", "tint-2": "#fbfbfc", "tint-3": "#f7f8f9",
        "rule-mid": "#8a6a2e", "reg-1": "#b8760f", "reg-2": "#d99b1c",
        "slot-b": "#b07a12", "slot-c": "#4a8560",
        "note-bg": "#fdf6e3", "note-br": "#f0e0b0", "note-ink": "#5c4a1c", "note-b": "#7a5e12",
    },
}

FILES = ["brochure.src.html", "agenda.src.html"]


def apply(name):
    pal = PALETTES[name]
    for fn in FILES:
        p = HERE / fn
        s = p.read_text()
        for k, v in pal.items():
            s = re.sub(r"(--%s:)\s*#[0-9a-fA-F]{6}" % re.escape(k), r"\g<1>" + v, s)
        p.write_text(s)
    return name


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--list":
        print("palettes:", ", ".join(PALETTES))
    else:
        print("applied:", apply(sys.argv[1]))
