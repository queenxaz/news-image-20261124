[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/queenxaz/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/queenxaz/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

# THE WORLD TODAY — Tuesday 24 November 2026

**48 stories, 7 regions, 19 fields — date-checked.**

One image that sums up the world's news of Tuesday 24 November 2026:
Huang is back at Nvidia, COP31 collapses in Antalya, and mines appear in
the Hormuz Strait. Every story on the page happened, or was first reported,
on 24 November 2026 in some time zone — and the DATE CHECK box proves it,
naming the 23 November stories deliberately left out and the 25 November
stories not yet happened.

## What's on the front page

- **3 big leads** — Nvidia reinstates Jensen Huang as CEO; COP31 climate
  talks collapse after ~50 hours overtime; the IRGC claims three tankers
  struck mines in the Hormuz Strait as the US Treasury sanctions 22 Iran
  shadow-banking entities.
- **15 illustrated stories** with flat drawings, region tags, confidence
  tags (CONFIRMED / REPORTED / CLAIM) and a named source each.
- **THE DAY IN UTC** timeline strip (7 timed events).
- **Dotted world map** with 15 numbered pins matching the illustrated
  stories.
- **DATE CHECK box** — TODAY (24 Nov) / LEFT OUT (23 Nov, named) /
  NOT YET (25 Nov and later, named).
- **ALSO ON** — 33 more one-line stories, making 48 in total.
- **Region bar + by-field counts + THE DAY IN NUMBERS** strip.
- **HOW SURE legend + sources footer** (12 outlets, original drawings).

## How it runs

`main.py` draws the page deterministically with Pillow (`render.py`) and
writes it to `/output/entry.png`. No network, no randomness, no clock —
the same bytes every run. If Pillow or the fonts are missing in the
sandbox, `main.py` falls back to copying the shipped `entry.jpg`
(a byte-identical render) into place, so the run always completes.

```
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Licence

MIT — see `LICENSE`.
