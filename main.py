#!/usr/bin/env python3
"""News-image entry: copy the front page to /output/entry.png.

Python 3.13, standard library only. The image itself is drawn by
render.py (PIL, run on the build machine) and shipped in this repo
as entry.png; this program just places it where the harness reads it.
Outside the sandbox, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy size mismatch")
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
