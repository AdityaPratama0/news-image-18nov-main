#!/usr/bin/env python3
"""Generate the 18 November 2026 world-news day strip."""
from __future__ import annotations

import html
import os
import subprocess
import sys
import tempfile

W, H = 1024, 1024
PAPER, INK, TEAL, GREY, WHITE = "#f7f4ec", "#17181a", "#0f6b6b", "#8a8578", "#ffffff"

STORIES = [
    ("MIDDLE EAST", "US strikes Iran's Qeshm Island", "Third attack on US sites in five days; tankers hit mines in Hormuz."),
    ("EUROPE", "Crimea Bridge road arch destroyed", "Kyiv presses deep strikes; Moscow promises a response."),
    ("ASIA-PACIFIC", "Quad leaders vow maritime and cyber pact", "Manila summit: Trump, Modi, Albanese and Takaichi."),
    ("UNITED STATES", "Nvidia ex-CEO seeks his job back", "Revenue $115.8bn as Huang asks the board to return."),
    ("AFRICA", "South Africa summons Nigeria's envoy", "Diplomatic demarche over his social media remarks."),
]

ALSO = [
    "Gaza truce warning", "US loses measles elimination status",
    "Microsoft 365 outage", "BBC, IKEA and Air France hack",
    "Alaska Senate result", "Haiti gangs and Salvadoran troops",
    "Mongolia president stepping down", "Japan PM meets Trump",
    "Seoul invited to Tokyo", "Bahraini activist dies",
    "Ecuador fishermen sue", "Japan lose to Paraguay",
    "Knesset elects speaker opposed to Netanyahu",
    "APEC leaders gather in Shenzhen",
    "Bangladesh says India cannot dictate Hasina's return",
    "Rare contact with Awa people in Brazil", "Tokyo bus dual pricing",
    "Delhi blast kills eight", "Russia says drone hit Moscow substation",
    "Nigeria church attack kills eight", "Israeli strike hits Lebanon camp",
    "Two dead in US campus shooting", "Republicans hold Tennessee seat",
    "APC wins Anambra governorship", "Gaza truce to start, Qatar says",
    "Trump says Venezuela talks stalled", "Avignon mass rape trial verdict",
    "Bowen ruled out of Ashes opener",
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def icon(n: int, x: int, y: int) -> str:
    """Bold, legible white pictograms centered in a 76 px teal tile."""
    cx, cy = x + 38, y + 38
    common = f'fill="none" stroke="{WHITE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'
    if n == 1:  # island, blast, strait
        return f'<path {common} d="M{x+14} {y+57}c12-12 23 3 34-5 7-5 11-2 15 3 M{x+14} {y+64}h49 M{cx} {y+11}v13 m-13-5 9 7 m17-7-9 7 M{cx} {y+27}l-5 8 5 8 5-8z"/>'
    if n == 2:  # broken bridge
        return f'<path {common} d="M{x+10} {y+56}h16l12-18 12 18h16 M{x+12} {y+63}v-16 M{x+64} {y+63}v-16 M{cx-5} {y+45}l10 9-9 10"/>'
    if n == 3:  # four nodes / maritime pact
        return f'<circle cx="{cx}" cy="{cy}" r="8" fill="{WHITE}"/><path {common} d="M{cx} {cy-8}V{y+14} M{cx+8} {cy}H{x+62} M{cx} {cy+8}V{y+62} M{cx-8} {cy}H{x+14}"/><circle {common} cx="{cx}" cy="{y+12}" r="5"/><circle {common} cx="{x+64}" cy="{cy}" r="5"/><circle {common} cx="{cx}" cy="{y+64}" r="5"/><circle {common} cx="{x+12}" cy="{cy}" r="5"/>'
    if n == 4:  # chip / return arrow
        return f'<rect {common} x="{x+22}" y="{y+22}" width="32" height="32" rx="3"/><path {common} d="M{x+30} {y+13}v9m10-9v9m10-9v9m-20 32v9m10-9v9m10-9v9 M{x+13} {y+30}h9m-9 10h9m-9 10h9m32-20h9m-9 10h9m-9 10h9 M{x+46} {y+45}a10 10 0 1 1-2-15 M{x+44} {y+30}l7-1-2-7"/>'
    return f'<path {common} d="M{x+12} {y+19}h34v25H{x+28}l-9 9v-9h-7z M{x+31} {y+38}h32v22H{x+55}v8l-9-8H{x+31}z M{x+20} {y+29}h18 M{x+39} {y+49}h16"/>'


def map_svg() -> str:
    with open("/tmp/mask.txt", encoding="ascii") as f:
        rows = f.read().splitlines()
    if len(rows) != 45 or any(len(row) != 90 for row in rows):
        raise ValueError("/tmp/mask.txt must be exactly 90x45")
    dots = []
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch == "#":
                dots.append(f'<circle cx="{278 + xx*5.15:.2f}" cy="{653 + yy*3.10:.2f}" r="1.95"/>')
    # approximate story locations: Gulf, Crimea, Manila, US, South Africa
    markers = [(574, 700), (540, 671), (655, 718), (357, 693), (531, 755)]
    ms = []
    for i, (x, y) in enumerate(markers, 1):
        ms.append(f'<circle cx="{x}" cy="{y}" r="9.2" fill="{TEAL}" stroke="{PAPER}" stroke-width="2"/><text x="{x}" y="{y+3.3}" text-anchor="middle" class="mark">{i}</text>')
    return f'<g fill="{GREY}" opacity=".96">{"".join(dots)}</g>{"".join(ms)}'


def svg() -> str:
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="1024" height="1024" fill="{PAPER}"/>
<style>
 .sans {{font-family:"DejaVu Sans",sans-serif; fill:{INK}}}
 .serif {{font-family:"DejaVu Serif",serif; fill:{INK}}}
 .region {{font-family:"DejaVu Sans",sans-serif;font-size:12px;font-weight:700;letter-spacing:1.8px;fill:{TEAL}}}
 .fact {{font-family:"DejaVu Sans",sans-serif;font-size:15px;fill:{GREY}}}
 .mark {{font-family:"DejaVu Sans",sans-serif;font-size:9px;font-weight:700;fill:white}}
</style>
<text class="sans" x="40" y="34" font-size="12" font-weight="700" letter-spacing="2.5">THE WORLD, WEDNESDAY</text>
<text class="serif" x="40" y="112" font-size="68" font-weight="700" textLength="944" lengthAdjust="spacingAndGlyphs">18 November 2026</text>
<path d="M40 139H984" stroke="{INK}" stroke-width="1.5"/>
''']
    for i, (region, headline, fact) in enumerate(STORIES, 1):
        y = 140 + (i - 1) * 98
        # headline size is selected per measured available line width; long item 3 is set smaller.
        hsize = 25 if i == 3 else 27
        out.append(f'<path d="M40 {y+97}H984" stroke="{GREY}" stroke-opacity=".35"/>')
        out.append(f'<rect x="40" y="{y+11}" width="76" height="76" rx="3" fill="{TEAL}"/>')
        out.append(icon(i, 40, y + 11))
        out.append(f'<text class="region" x="140" y="{y+20}">{esc(region)}</text>')
        out.append(f'<text class="serif" x="140" y="{y+53}" font-size="{hsize}" font-weight="700">{esc(headline)}</text>')
        out.append(f'<text class="fact" x="140" y="{y+78}">{esc(fact)}</text>')
    out.append(f'''<text class="sans" x="40" y="639" font-size="12" font-weight="700" letter-spacing="1.8" fill="{TEAL}">THE DAY IN PLACE</text>
{map_svg()}
<text class="sans" x="40" y="807" font-size="12" font-weight="700" letter-spacing="1.8" fill="{TEAL}">ALSO TODAY · 18 NOVEMBER 2026</text>''')
    for idx, item in enumerate(ALSO, 6):
        col = 0 if idx < 20 else 1
        row = idx - 6 if col == 0 else idx - 20
        x = 40 + col * 482
        y = 824 + row * 11.5
        out.append(f'<rect x="{x}" y="{y-9.5}" width="462" height="11" fill="none" stroke="{GREY}" stroke-opacity=".30"/>')
        out.append(f'<text class="sans" x="{x+6}" y="{y}" font-size="10.2"><tspan fill="{TEAL}" font-weight="700">{idx}</tspan><tspan dx="5">{esc(item)}</tspan></text>')
    out.append(f'''<path d="M40 984H984" stroke="{INK}" stroke-width="1"/>
<text class="sans" x="40" y="1005" font-size="9.5" fill="{GREY}">SOURCES  Reuters · AP · BBC · AFP · official statements</text>
<text class="sans" x="984" y="1005" text-anchor="end" font-size="9.5" font-weight="700">18 NOVEMBER 2026</text>
</svg>''')
    return "".join(out)


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    data = svg().encode()
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
        f.write(data)
        temp = f.name
    try:
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", output, temp], check=True)
    finally:
        os.unlink(temp)


if __name__ == "__main__":
    main()
