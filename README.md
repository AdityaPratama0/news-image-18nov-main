# The World Today

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/AdityaPratama0/news-image-18nov-main/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/AdityaPratama0/news-image-18nov-main/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program-drawn newspaper front page for 18 November 2026. Six illustrated lead cards form the front-page grid, followed by 27 compact briefs in three ruled columns. Together they present all 33 stories with a traditional masthead, restrained editorial typography, and a warm-paper, ink, deep-crimson, warm-grey, and white palette.

The artwork is generated as deterministic SVG geometry and typography using only the Python standard library, then rasterised to a 1024 × 1024 PNG with `rsvg-convert`. It does not require the optional map mask or network access.

## Regenerate

From this directory, with Python 3, `rsvg-convert`, DejaVu fonts, Node, and ImageMagick installed:

```sh
python3 gen.py entry.png
identify entry.png
mkdir -p /tmp/np
MAKEFUN_OUTPUT_DIR=/tmp/np node main.ts
sha256sum entry.png /tmp/np/entry.png
```

For a readability check at the target preview size:

```sh
convert entry.png -resize 480x480 /tmp/front-page-480.png
identify /tmp/front-page-480.png
```
