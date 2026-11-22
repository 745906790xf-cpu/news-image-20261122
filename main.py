#!/usr/bin/env python3
"""make.fun entry for news-image-20261122 (Python 3.13, standard library only).

The entry's image is poster.png beside this file (drawn by render_poster.py);
this program copies it to /output/entry.png. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

here = Path(__file__).resolve().parent
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(here / "poster.png", out_dir / "entry.png")
