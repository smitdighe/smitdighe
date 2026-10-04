"""Build the README's Pac-Man graph from the dark variant only.

The profile is dark-themed on purpose: light-mode visitors get the same dark
graph, framed on a rounded dark card like the other README images.
"""
import re
from pathlib import Path

ASSETS = Path("assets")
DARK = ASSETS / "pacman-contribution-graph-dark.svg"
OUT = ASSETS / "pacman-contribution-graph-auto.svg"
BG = "#0d1117"
PAD = 14

ROOT_RE = re.compile(r"<svg\b([^>]*)>(.*)</svg>\s*$", re.S)


def split_root(text):
    match = ROOT_RE.search(text)
    if not match:
        raise SystemExit("no <svg> root found")
    attrs, body = match.group(1), match.group(2)
    width = re.search(r'\bwidth="([\d.]+)"', attrs)
    height = re.search(r'\bheight="([\d.]+)"', attrs)
    if not (width and height):
        raise SystemExit("root <svg> missing width/height")
    return float(width.group(1)), float(height.group(1)), body


def main():
    w, h, body = split_root(DARK.read_text(encoding="utf-8"))
    ow, oh = w + 2 * PAD, h + 2 * PAD
    OUT.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" width="%g" height="%g" '
        'viewBox="0 0 %g %g" role="img" aria-label="Pac-Man contribution graph">'
        '<rect width="%g" height="%g" rx="10" fill="%s"/>'
        '<svg x="%d" y="%d" width="%g" height="%g" viewBox="0 0 %g %g">%s</svg>'
        "</svg>\n" % (ow, oh, ow, oh, ow, oh, BG, PAD, PAD, w, h, w, h, body),
        encoding="utf-8",
    )
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
