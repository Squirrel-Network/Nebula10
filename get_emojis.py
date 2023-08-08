#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import io
import pathlib

import requests
from bs4 import BeautifulSoup
from PIL import Image

from core.utilities import emoji

EMOJIPEDIA_URL = "https://emojipedia.org/apple/"


def main():
    path = pathlib.Path("resources/emojis")
    path.mkdir(parents=True, exist_ok=True)

    resp = requests.get(EMOJIPEDIA_URL).text
    soup = BeautifulSoup(resp, "html.parser")

    for x in soup.find(class_="emoji-grid").find_all("img"):
        img: str = x.get("data-src") or x.get("src")
        name = img.split("/")[-1].split("_")[0].upper().replace("-", "_")

        if not getattr(emoji, name, None):
            continue

        image = Image.open(io.BytesIO(requests.get(img).content))
        img_path = path / f"{name}.png"

        image.resize((100, 100)).convert("RGBA").save(img_path)

    print("Done!")


if __name__ == "__main__":
    main()
