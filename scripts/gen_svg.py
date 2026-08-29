import json
import math
import os
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

LOGIN = os.environ.get("GH_LOGIN", "smitdighe")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path("assets")

ACCENT = "#FF7B54"
ACCENT_2 = "#FFB26B"
ACCENT_3 = "#7AA2F7"

THEME_CSS = """
  .fg    { fill: #1f2328; }
  .muted { fill: #59636e; }
  .card  { fill: #ffffff; stroke: #d1d9e0; }
  .grid  { stroke: #d1d9e0; }
  @media (prefers-color-scheme: dark) {
    .fg    { fill: #e6edf3; }
    .muted { fill: #9198a1; }
    .card  { fill: #161b22; stroke: #30363d; }
    .grid  { stroke: #30363d; }
  }
"""

FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


GRAPHQL = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_calendar():
    if not TOKEN:
        print("no GITHUB_TOKEN, skipping contribution fetch")
        return []
    body = json.dumps({"query": GRAPHQL, "variables": {"login": LOGIN}})
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body.encode("utf-8"),
        headers={
            "Authorization": "bearer " + TOKEN,
            "Content-Type": "application/json",
            "User-Agent": LOGIN + "-readme-bot",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as err:
        print("contribution fetch failed:", err)
        return []

    user = payload.get("data", {}).get("user")
    if not user:
        print("unexpected payload:", payload)
        return []

    days = []
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    for week in weeks:
        for day in week["contributionDays"]:
            days.append((day["date"], day["contributionCount"]))
    return days


def monthly_totals(days):
    buckets = {}
    for iso, count in days:
        key = iso[:7]
        buckets[key] = buckets.get(key, 0) + count

    today = date.today()
    keys = []
    year = today.year
    month = today.month
    for _ in range(12):
        keys.append("%04d-%02d" % (year, month))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    keys.reverse()

    out = []
    for key in keys:
        out.append((key, buckets.get(key, 0)))
    return out


SUBTITLES = [
    "Full-Stack Dev &#183; AI/ML Builder",
    "LangChain &#183; RAG &#183; Multi-Agent Systems",
    "Trained ML models &#8594; deployed products",
    "Open to opportunities",
]

SUB_START = 2.6
SUB_SLOT = 3.5
SUB_FADE = 0.5
SUB_LOOP = SUB_SLOT * len(SUBTITLES)


def write_header():
    w, h = 900, 190
    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="img" aria-label="Smit Dighe">' % (w, h, w, h)
    )
    parts.append("<style>%s .t{font-family:%s}</style>" % (THEME_CSS, FONT))

    parts.append(
        '<defs>'
        '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%%" stop-color="%s"><animate attributeName="offset" '
        'values="-0.4;0.6;-0.4" dur="7s" repeatCount="indefinite"/></stop>'
        '<stop offset="50%%" stop-color="%s"><animate attributeName="offset" '
        'values="0;1;0" dur="7s" repeatCount="indefinite"/></stop>'
        '<stop offset="100%%" stop-color="%s"><animate attributeName="offset" '
        'values="0.4;1.4;0.4" dur="7s" repeatCount="indefinite"/></stop>'
        '</linearGradient>'
        '</defs>' % (ACCENT, ACCENT_2, ACCENT_3)
    )

    for i in range(26):
        cx = (i * 137) % w
        cy = 18 + ((i * 61) % (h - 36))
        r = 1.2 + (i % 3) * 0.7
        dur = 9 + (i % 7) * 2
        parts.append(
            '<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="0.25">'
            '<animate attributeName="cy" values="%d;%d;%d" dur="%ds" '
            'repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values="0.05;0.4;0.05" dur="%ds" '
            'repeatCount="indefinite"/></circle>'
            % (cx, cy, r, ACCENT, cy, cy - 26, cy, dur, dur)
        )

    parts.append(
        '<text class="t" x="450" y="92" text-anchor="middle" font-size="62" '
        'font-weight="700" fill="none" stroke="url(#g)" stroke-width="1.6" '
        'stroke-dasharray="1200" stroke-dashoffset="1200">'
        'Smit Dighe'
        '<animate attributeName="stroke-dashoffset" from="1200" to="0" dur="2.6s" '
        'fill="freeze"/>'
        '<animate attributeName="fill" from="rgba(255,123,84,0)" to="%s" '
        'begin="2.2s" dur="1.2s" fill="freeze"/>'
        '</text>' % ACCENT
    )

    keys = "0;%.4f;%.4f;%.4f;1" % (
        SUB_FADE / SUB_LOOP,
        (SUB_SLOT - SUB_FADE) / SUB_LOOP,
        SUB_SLOT / SUB_LOOP,
    )
    for index, line in enumerate(SUBTITLES):
        parts.append(
            '<text class="t muted" x="450" y="128" text-anchor="middle" '
            'font-size="17" opacity="0">%s'
            '<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="%s" '
            'dur="%.1fs" begin="%.2fs" repeatCount="indefinite"/></text>'
            % (line, keys, SUB_LOOP, SUB_START + index * SUB_SLOT)
        )

    parts.append(
        '<rect x="300" y="146" width="0" height="2.5" rx="1.25" fill="url(#g)">'
        '<animate attributeName="width" from="0" to="300" begin="3.1s" dur="0.8s" '
        'fill="freeze"/></rect>'
    )

    parts.append("</svg>")
    (OUT / "header.svg").write_text("\n".join(parts), encoding="utf-8")


RINGS = [
    (110, 26, False, 90, ["Python", "TypeScript", "C"]),
    (185, 36, True, 36, ["React", "FastAPI", "Node.js", "Flask", "Express"]),
    (258, 48, False, 15,
     ["LangChain", "LangGraph", "Postgres", "Docker", "n8n", "Groq"]),
]


def write_orbit():
    size = 640
    c = size / 2
    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="img" aria-label="Tech stack orbit">'
        % (size, size, size, size)
    )
    parts.append("<style>%s .t{font-family:%s}</style>" % (THEME_CSS, FONT))

    for radius, _dur, _rev, _phase, _items in RINGS:
        parts.append(
            '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" class="grid" '
            'stroke-width="1" stroke-dasharray="3 6" opacity="0.7"/>'
            % (c, c, radius)
        )

    parts.append(
        '<circle cx="%.1f" cy="%.1f" r="46" fill="%s" opacity="0.14">'
        '<animate attributeName="r" values="42;52;42" dur="4s" '
        'repeatCount="indefinite"/></circle>' % (c, c, ACCENT)
    )
    parts.append(
        '<circle cx="%.1f" cy="%.1f" r="34" fill="%s"/>' % (c, c, ACCENT)
    )
    parts.append(
        '<text class="t" x="%.1f" y="%.1f" text-anchor="middle" font-size="13" '
        'font-weight="700" fill="#ffffff">smit</text>' % (c, c + 4)
    )

    for ring in RINGS:
        radius, dur, reverse, phase, items = ring
        start = "360" if reverse else "0"
        end = "0" if reverse else "360"
        parts.append(
            '<g><animateTransform attributeName="transform" type="rotate" '
            'from="%s %.1f %.1f" to="%s %.1f %.1f" dur="%ds" '
            'repeatCount="indefinite"/>' % (start, c, c, end, c, c, dur)
        )
        count = len(items)
        for index, label in enumerate(items):
            angle = (2 * math.pi * index) / count + math.radians(phase)
            x = c + radius * math.cos(angle)
            y = c + radius * math.sin(angle)
            width = 16 + 8.0 * len(label)
            counter_from = "0" if reverse else "0"
            counter_to = "360" if reverse else "-360"
            parts.append('<g transform="translate(%.1f,%.1f)">' % (x, y))
            parts.append(
                '<g><animateTransform attributeName="transform" type="rotate" '
                'from="%s 0 0" to="%s 0 0" dur="%ds" repeatCount="indefinite"/>'
                % (counter_from, counter_to, dur)
            )
            parts.append(
                '<rect class="card" x="%.1f" y="-13" width="%.1f" height="26" '
                'rx="13" stroke-width="1"/>' % (-width / 2, width)
            )
            parts.append(
                '<text class="t fg" x="0" y="5" text-anchor="middle" '
                'font-size="12">%s</text>' % label
            )
            parts.append("</g></g>")
        parts.append("</g>")

    parts.append("</svg>")
    (OUT / "orbit.svg").write_text("\n".join(parts), encoding="utf-8")


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def write_commit_race(totals):
    w, h = 900, 280
    left, right = 44, 24
    top, bottom = 46, 52
    plot_w = w - left - right
    plot_h = h - top - bottom
    slot = plot_w / 12.0
    bar_w = slot * 0.56

    peak = 1
    for _key, value in totals:
        if value > peak:
            peak = value

    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="img" aria-label="Contributions per month">'
        % (w, h, w, h)
    )
    parts.append("<style>%s .t{font-family:%s}</style>" % (THEME_CSS, FONT))
    parts.append(
        '<defs><linearGradient id="bar" x1="0" y1="1" x2="0" y2="0">'
        '<stop offset="0%%" stop-color="%s" stop-opacity="0.55"/>'
        '<stop offset="100%%" stop-color="%s"/></linearGradient></defs>'
        % (ACCENT, ACCENT_2)
    )

    parts.append(
        '<text class="t fg" x="%d" y="26" font-size="15" font-weight="700">'
        'Contributions &#183; last 12 months</text>' % left
    )

    for step in range(4):
        y = top + (plot_h / 3.0) * step
        value = int(round(peak - (peak / 3.0) * step))
        parts.append(
            '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="grid" '
            'stroke-width="1" opacity="0.5"/>' % (left, y, w - right, y)
        )
        parts.append(
            '<text class="t muted" x="%d" y="%.1f" font-size="10" '
            'text-anchor="end">%d</text>' % (left - 8, y + 3, value)
        )

    for index, item in enumerate(totals):
        key, value = item
        bar_h = (value / float(peak)) * plot_h
        x = left + slot * index + (slot - bar_w) / 2.0
        y = top + plot_h - bar_h
        delay = 0.15 + index * 0.07
        parts.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="0" rx="4" fill="url(#bar)">'
            '<animate attributeName="height" from="0" to="%.1f" begin="%.2fs" '
            'dur="0.9s" fill="freeze" calcMode="spline" keySplines="0.2 0 0 1" '
            'keyTimes="0;1"/>'
            '<animate attributeName="y" from="%.1f" to="%.1f" begin="%.2fs" '
            'dur="0.9s" fill="freeze" calcMode="spline" keySplines="0.2 0 0 1" '
            'keyTimes="0;1"/></rect>'
            % (x, top + plot_h, bar_w, bar_h, delay, top + plot_h, y, delay)
        )
        parts.append(
            '<text class="t fg" x="%.1f" y="%.1f" font-size="11" '
            'text-anchor="middle" opacity="0">%d'
            '<animate attributeName="opacity" from="0" to="1" begin="%.2fs" '
            'dur="0.5s" fill="freeze"/></text>'
            % (x + bar_w / 2.0, y - 7, value, delay + 0.7)
        )
        month_index = int(key[5:7]) - 1
        parts.append(
            '<text class="t muted" x="%.1f" y="%d" font-size="11" '
            'text-anchor="middle">%s</text>'
            % (x + bar_w / 2.0, top + plot_h + 20, MONTH_NAMES[month_index])
        )

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts.append(
        '<text class="t muted" x="%d" y="%d" font-size="10" text-anchor="end">'
        'generated %s</text>' % (w - right, h - 12, stamp)
    )

    parts.append("</svg>")
    (OUT / "commit-race.svg").write_text("\n".join(parts), encoding="utf-8")


def write_divider():
    w, h = 900, 12
    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="presentation">' % (w, h, w, h)
    )
    parts.append(
        '<defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%%" stop-color="%s" stop-opacity="0"/>'
        '<stop offset="50%%" stop-color="%s" stop-opacity="0.9"/>'
        '<stop offset="100%%" stop-color="%s" stop-opacity="0"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'from="-1 0" to="1 0" dur="5s" repeatCount="indefinite"/>'
        '</linearGradient></defs>' % (ACCENT, ACCENT_2, ACCENT_3)
    )
    parts.append(
        '<rect x="0" y="5" width="%d" height="2" rx="1" fill="#888" '
        'opacity="0.18"/>' % w
    )
    parts.append('<rect x="0" y="4.5" width="%d" height="3" rx="1.5" fill="url(#d)"/>' % w)
    parts.append("</svg>")
    (OUT / "divider.svg").write_text("\n".join(parts), encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    write_header()
    write_orbit()
    write_divider()

    days = fetch_calendar()
    if days:
        write_commit_race(monthly_totals(days))
    else:
        target = OUT / "commit-race.svg"
        if not target.exists():
            write_commit_race(monthly_totals([]))
        else:
            print("keeping existing commit-race.svg")

    print("done")


if __name__ == "__main__":
    main()
