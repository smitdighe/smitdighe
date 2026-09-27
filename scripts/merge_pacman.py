"""Merge the light + dark Pac-Man SVGs into one theme-adaptive SVG.

GitHub's <picture> + prefers-color-scheme follows the OS setting, not the
GitHub theme, so a dark GitHub page on a light OS shows the light file.
A single SVG that switches via an internal @media rule follows the page's
color-scheme instead (same mechanism as orbit.svg / header.svg).
"""
import re
from pathlib import Path

ASSETS = Path("assets")
LIGHT = ASSETS / "pacman-contribution-graph.svg"
DARK = ASSETS / "pacman-contribution-graph-dark.svg"
OUT = ASSETS / "pacman-contribution-graph-auto.svg"

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


def prefix_ids(body, prefix):
    body = re.sub(r'\bid="([^"]+)"', r'id="%s\1"' % prefix, body)
    body = re.sub(r'((?:xlink:)?href)="#([^"]+)"', r'\1="#%s\2"' % prefix, body)
    body = re.sub(r"url\(#([^)]+)\)", r"url(#%s\1)" % prefix, body)
    return body


def main():
    lw, lh, light = split_root(LIGHT.read_text(encoding="utf-8"))
    dw, dh, dark = split_root(DARK.read_text(encoding="utf-8"))
    w, h = max(lw, dw), max(lh, dh)
    light = prefix_ids(light, "l-")
    dark = prefix_ids(dark, "d-")
    box = 'width="%g" height="%g" viewBox="0 0 %g %g"' % (w, h, w, h)
    OUT.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" %s role="img" '
        'aria-label="Pac-Man contribution graph">'
        "<style>.pm-dark{display:none}"
        "@media (prefers-color-scheme: dark){.pm-light{display:none}.pm-dark{display:inline}}"
        "</style>"
        '<svg class="pm-light" %s>%s</svg>'
        '<svg class="pm-dark" %s>%s</svg>'
        "</svg>\n" % (box, box, light, box, dark),
        encoding="utf-8",
    )
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
