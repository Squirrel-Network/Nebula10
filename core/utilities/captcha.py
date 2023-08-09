#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import io
import os
import pathlib
import random

from Crypto.Cipher import AES
from PIL import Image

from config import Session

MAX_EMOJI = 15
MAX_EMOJI_CORRECT = 6
IMAGE_POSITION = (
    (38, 45),
    (215, 45),
    (392, 45),
    (38, 235),
    (215, 235),
    (392, 235),
)


def encrypt_data(correct: bool, mistakes: int, user_id: int) -> bytes:
    data = (
        correct.to_bytes(1, "little")
        + mistakes.to_bytes(1, "little")
        + user_id.to_bytes(4, "little")
    )

    block_size = AES.block_size * 4
    data += os.urandom(block_size - len(data))

    cipher = AES.new(
        bytes(Session.config.TOKEN_SECRET, "utf-8"), AES.MODE_CBC, bytes(16)
    )
    ciphertext = cipher.encrypt(data)

    return ciphertext


def decrypt_data(ciphertext: bytes) -> tuple[bool, int, int]:
    decipher = AES.new(
        bytes(Session.config.TOKEN_SECRET, "utf-8"), AES.MODE_CBC, bytes(16)
    )
    decrypted_data = decipher.decrypt(ciphertext)

    return (
        bool(decrypted_data[0]),
        decrypted_data[1],
        int.from_bytes(decrypted_data[2:6], "little"),
    )


def get_image(correct_emoji: list[str], emoji_path: pathlib.Path):
    background = Image.open(
        pathlib.Path("resources") / "background" / "background.png"
    ).convert("RGBA")
    correct_emoji = [pathlib.Path(emoji_path / f"{x}.png") for x in correct_emoji]
    emojis = []

    for image_name in correct_emoji:
        image = Image.open(image_name).convert("RGBA")
        emojis.append(image)

    for image, position in zip(emojis, IMAGE_POSITION):
        rotation_angle = random.randint(0, 360)
        rotated_image = image.rotate(rotation_angle, expand=True)

        background.paste(rotated_image, position, rotated_image)

    result_bytes_io = io.BytesIO()

    background.save(result_bytes_io, format="PNG")

    result_bytes_io.seek(0)

    return result_bytes_io


def get_catcha(user_id: int):
    path = pathlib.Path("resources") / "emojis"

    all_emoji = random.sample([x.stem for x in path.glob("*.png")], MAX_EMOJI)
    correct_emoji = random.sample(all_emoji, MAX_EMOJI_CORRECT)

    return get_image(correct_emoji, path)
