"""Entrypoint for the news-image-20261127 bounty.

Renders the 27 November 2026 front page (see draw.py) and writes the single
required image to /output/entry.png. Deterministic: no network, no clock,
no randomness — two runs produce byte-identical PNGs.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import render


def main():
    image = render()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    image.save(out_path, format="PNG")
    with open(out_path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("wrote {} {}x{} sha256 {}".format(
        out_path, image.size[0], image.size[1], digest))


if __name__ == "__main__":
    main()
