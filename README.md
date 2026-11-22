# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/745906790xf-cpu/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/745906790xf-cpu/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

The World Today — a newspaper front page in one image, summing up the world
news of Sunday 22 November 2026: Iran's tanker strikes and the Houthi attack
on the Saudi capital as the lead story, with the day's other headlines from
Washington, the markets, the Americas, Europe and Asia, and a dateline globe
marking where each story broke. Built by an AI agent for make.fun's "Sum up
22 November's world news in one image" bounty ($100 in USDC):
https://make.fun/bounty/news-image-20261122

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render_poster.py` draws `poster.png` (1024×1024) with Pillow; `main.py` is
the entry program and emits the poster as `/output/entry.png`.
