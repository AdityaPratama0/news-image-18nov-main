# Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)

A program-drawn broadsheet front page covering 45 Wednesday stories across seven regions. Its story budget is 13 large illustrated news cards, each with a distinct flat-vector scene, plus 32 ruled briefs. Proportional region tabs, a pinned dot map, numeric ticker, date-check panel, and source line provide the front-page navigation and verification layer.

The artwork is deterministic SVG geometry and measured typography generated with the Python standard library, then rasterised by `rsvg-convert`. The only input asset is the supplied `/tmp/mask.txt` land mask.

## Regenerate

```sh
python3 gen.py entry.png
identify entry.png
mkdir -p /tmp/np
MAKEFUN_OUTPUT_DIR=/tmp/np node main.ts
sha256sum entry.png /tmp/np/entry.png
```

Preview checks:

```sh
convert entry.png -resize 480x480 /tmp/front-page-480.png
convert entry.png -resize 300x300 /tmp/front-page-300.png
```
