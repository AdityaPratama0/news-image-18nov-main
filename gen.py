#!/usr/bin/env python3
"""Draw a newspaper front page for 18 November 2026."""
from __future__ import annotations

import html
import os
import subprocess
import sys
import tempfile

W = H = 1024
PAPER, INK, CRIMSON, GREY, WHITE = "#f7f3e8", "#161616", "#8f1d1d", "#7d7668", "#ffffff"

LEADS = [
    ("MIDDLE EAST", "US strikes Iran's Qeshm Island", "Third attack on US sites in five days; tankers hit mines in Hormuz."),
    ("EUROPE", "Crimea Bridge road arch destroyed", "Kyiv presses deep strikes; Moscow promises a response."),
    ("ASIA-PACIFIC", "Quad leaders vow maritime and cyber pact", "Manila summit: Trump, Modi, Albanese and Takaichi."),
    ("UNITED STATES", "Nvidia ex-CEO seeks his job back", "Revenue $115.8bn as Huang asks the board to return."),
    ("AFRICA", "South Africa summons Nigeria's envoy", "Diplomatic demarche over his social media remarks."),
    ("GAZA", "Truce to start, Qatar says", "Mediators announce a start date as strikes continue."),
]

BRIEFS = [
    "Gaza truce warning", "US loses measles elimination status", "Microsoft 365 outage",
    "BBC, IKEA and Air France hack", "Alaska Senate result", "Haiti gangs and Salvadoran troops",
    "Mongolia president stepping down", "Japan PM meets Trump", "Seoul invited to Tokyo",
    "Bahraini activist dies", "Ecuador fishermen sue", "Japan lose to Paraguay",
    "Knesset elects speaker opposed to Netanyahu", "APEC leaders gather in Shenzhen",
    "Bangladesh says India cannot dictate Hasina's return", "Rare contact with Awa people in Brazil",
    "Tokyo bus dual pricing", "Delhi blast kills eight", "Russia says drone hit Moscow substation",
    "Nigeria church attack kills eight", "Israeli strike hits Lebanon camp",
    "Two dead in US campus shooting", "Republicans hold Tennessee seat",
    "APC wins Anambra governorship", "Trump says Venezuela talks stalled",
    "Avignon mass rape trial verdict", "Bowen ruled out of Ashes opener",
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def fitted_text(text: str, x: float, y: float, max_width: float, size: float, css: str) -> str:
    """Apply textLength only when a conservative width estimate exceeds the box."""
    estimate = len(text) * size * (0.57 if "sans" in css else 0.59)
    fit = f' textLength="{max_width:.1f}" lengthAdjust="spacingAndGlyphs"' if estimate > max_width else ""
    return f'<text class="{css}" x="{x}" y="{y}" font-size="{size}"{fit}>{esc(text)}</text>'


def icon(number: int, x: int, y: int) -> str:
    """Six high-contrast editorial pictograms in 54-pixel tiles."""
    s = f'fill="none" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    if number == 1:
        body = f'<path {s} d="M{x+9} {y+38}c8-8 14 2 21-3 6-4 10-1 15 3M{x+9} {y+44}h36M{x+28} {y+8}v10m-8-6 6 6m10-6-6 6M{x+28} {y+20}l-4 6 4 6 4-6z"/>'
    elif number == 2:
        body = f'<path {s} d="M{x+7} {y+39}h11l9-14 9 14h11M{x+9} {y+45}V{y+34}m36 11V{y+34}M{x+24} {y+31}l8 7-7 8"/>'
    elif number == 3:
        body = f'<circle {s} cx="{x+27}" cy="{y+27}" r="14"/><path {s} d="M{x+27} {y+8}v7m0 24v7M{x+8} {y+27}h7m24 0h7M{x+21} {y+33}l4-10 10-4-4 10z"/>'
    elif number == 4:
        body = f'<rect {s} x="{x+15}" y="{y+15}" width="25" height="25"/><path {s} d="M{x+20} {y+9}v6m8-6v6m8-6v6m-16 25v6m8-6v6m8-6v6M{x+9} {y+20}h6m-6 8h6m-6 8h6m25-16h6m-6 8h6m-6 8h6M{x+34} {y+31}a8 8 0 1 1-2-11m0 0 6 1-1-6"/>'
    elif number == 5:
        body = f'<path {s} d="M{x+13} {y+8}v38M{x+14} {y+11}h29l-7 8 7 8H{x+14}M{x+8} {y+46}h12M{x+24} {y+35}h19m-5-4 5 4-5 4"/>'
    else:
        body = f'<path {s} d="M{x+8} {y+30}c12 2 15-8 20-17 1 8 5 12 15 12-4 10-12 16-23 13l-7 6 2-9c-4-1-6-3-7-5zM{x+34} {y+26}l11-6"/>'
    return f'<rect x="{x}" y="{y}" width="54" height="54" fill="{CRIMSON}"/>{body}'


def headline_lines(number: int) -> list[str]:
    return {
        1: ["US strikes Iran's", "Qeshm Island"], 2: ["Crimea Bridge road", "arch destroyed"],
        3: ["Quad leaders vow maritime", "and cyber pact"], 4: ["Nvidia ex-CEO seeks", "his job back"],
        5: ["South Africa summons", "Nigeria's envoy"], 6: ["Truce to start, Qatar says"],
    }[number]


def make_svg() -> str:
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<rect width="1024" height="1024" fill="{PAPER}"/>
<style>
.sans {{font-family:"DejaVu Sans",sans-serif;fill:{INK}}}
.heavy {{font-family:"DejaVu Serif",serif;fill:{INK};font-weight:700}}
.region {{font-family:"DejaVu Sans",sans-serif;fill:{CRIMSON};font-weight:700;letter-spacing:1.5px}}
.fact {{font-family:"DejaVu Sans",sans-serif;fill:{GREY}}}
</style>
<path d="M40 19H984M40 91H984" stroke="{INK}" stroke-width="1"/>
<text class="sans" x="40" y="37" font-size="10" font-weight="700" letter-spacing="1.8">WEDNESDAY</text>
<text class="sans" x="984" y="37" text-anchor="end" font-size="10" font-weight="700" letter-spacing="1.2">18 NOVEMBER 2026</text>
<text class="heavy" x="40" y="79" font-size="49" textLength="944" lengthAdjust="spacingAndGlyphs">THE WORLD TODAY</text>
<text class="sans" x="40" y="108" font-size="11" font-weight="700" letter-spacing="1.2">33 STORIES FROM SIX CONTINENTS</text>
<text class="heavy" x="40" y="171" font-size="67" textLength="944" lengthAdjust="spacingAndGlyphs">18 November 2026</text>
<path d="M40 184H984" stroke="{INK}" stroke-width="2"/>
''']
    card_top, card_h = 195, 127
    for i, (region, _headline, fact) in enumerate(LEADS, 1):
        col, row = (i - 1) % 2, (i - 1) // 2
        x, y = 40 + col * 482, card_top + row * card_h
        if col:
            out.append(f'<path d="M512 {y}V{y+115}" stroke="{GREY}"/>')
        if row:
            out.append(f'<path d="M{x} {y}H{x+462}" stroke="{GREY}"/>')
        out.append(icon(i, x, y + 18))
        tx = x + 68
        out.append(f'<text class="region" x="{tx}" y="{y+24}" font-size="10">{esc(region)}</text>')
        for line_no, line in enumerate(headline_lines(i)):
            out.append(fitted_text(line, tx, y + 49 + line_no * 22, 392, 19 if i == 3 else 20, "heavy"))
        out.append(fitted_text(fact, tx, y + 101, 392, 10.8, "fact sans"))
    out.append(f'''<path d="M40 576H984" stroke="{INK}" stroke-width="2"/>
<rect x="40" y="588" width="112" height="25" fill="{CRIMSON}"/>
<text x="96" y="605" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="11" font-weight="700" letter-spacing="1.3" fill="{WHITE}">ALSO TODAY</text>
<text class="sans" x="984" y="605" text-anchor="end" font-size="9.5" font-weight="700" letter-spacing="1">27 BRIEFS · WORLD DESK</text>
''')
    col_width, row_h, brief_top = 292, 38, 623
    for offset, brief in enumerate(BRIEFS):
        col, row = offset // 9, offset % 9
        x, y = 40 + col * 326, brief_top + row * row_h
        out.append(f'<path d="M{x} {y+31}H{x+col_width}" stroke="{GREY}" stroke-width="0.7"/>')
        if col:
            out.append(f'<path d="M{x-11} {y-5}V{y+31}" stroke="{GREY}" stroke-width="0.7"/>')
        out.append(f'<text class="sans" x="{x}" y="{y+18}" font-size="11.3" fill="{CRIMSON}" font-weight="700">{offset+7:02d}</text>')
        out.append(fitted_text(brief, x + 25, y + 18, col_width - 25, 11.3, "sans"))
    out.append(f'''<path d="M40 976H984" stroke="{INK}" stroke-width="1.5"/>
<text class="fact" x="40" y="997" font-size="9.5">SOURCES · Reuters · AP · BBC · AFP · official statements</text>
<text class="sans" x="984" y="997" text-anchor="end" font-size="9.5" font-weight="700">18 NOVEMBER 2026</text>
</svg>''')
    return "".join(out)


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp:
        temp.write(make_svg().encode("utf-8"))
        temp_path = temp.name
    try:
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", output, temp_path], check=True)
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    main()
