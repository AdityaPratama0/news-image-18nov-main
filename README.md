# The World, Wednesday
[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/AdityaPratama0/news-image-18nov-main/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/AdityaPratama0/news-image-18nov-main/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program-drawn vertical day-strip summarising world news for 18 November 2026. Five lead stories form the timeline; numbered markers connect them to a dotted world map, while twenty-eight smaller developments complete the day.

The palette is deliberately restrained: warm paper, near-black ink, teal wayfinding, and warm-grey secondary detail. The illustration is generated as SVG geometry and typography, then rasterised deterministically with `rsvg-convert`.

## Regenerate

From this directory, with Python 3, `rsvg-convert`, DejaVu fonts, Node 22, ImageMagick, and `/tmp/mask.txt` available:

```sh
python3 gen.py entry.png
identify entry.png
mkdir -p /tmp/nim
MAKEFUN_OUTPUT_DIR=/tmp/nim node main.ts
sha256sum entry.png /tmp/nim/entry.png
```

No network access or third-party language packages are used.
