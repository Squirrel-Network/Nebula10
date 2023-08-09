#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import base64
import io
import os
import pathlib
import random

from Crypto.Cipher import AES
from PIL import Image
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import Session
from core.utilities import emoji
from core.utilities.menu import build_menu

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


def encrypt_data(correct: bool, mistakes: int, tot_correct: int, user_id: int) -> str:
    data = (
        correct.to_bytes(1, "little")
        + mistakes.to_bytes(1, "little")
        + tot_correct.to_bytes(1, "little")
        + user_id.to_bytes(4, "little")
    )

    block_size = AES.block_size
    data += os.urandom(block_size - len(data))

    cipher = AES.new(
        bytes(Session.config.TOKEN_SECRET, "utf-8"), AES.MODE_CBC, bytes(16)
    )
    ciphertext = cipher.encrypt(data)

    return base64.b64encode(ciphertext).decode("utf-8")


def decrypt_data(ciphertext: str) -> tuple[bool, int, int, int]:
    decipher = AES.new(
        bytes(Session.config.TOKEN_SECRET, "utf-8"), AES.MODE_CBC, bytes(16)
    )
    decrypted_data = decipher.decrypt(base64.b64decode(ciphertext))

    return (
        bool(decrypted_data[0]),
        decrypted_data[1],
        decrypted_data[2],
        int.from_bytes(decrypted_data[3:7], "little"),
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


def get_keyboard(
    all_emoji: list[str], correct_emoji: list[str], user_id: int
) -> InlineKeyboardMarkup:
    keyboard = [
        InlineKeyboardButton(
            getattr(emoji, x),
            callback_data=f"captcha|{encrypt_data(x in correct_emoji, 0, 0, user_id)}",
        )
        for x in all_emoji
    ]

    return InlineKeyboardMarkup(build_menu(keyboard, 5))


def get_catcha(user_id: int) -> tuple[io.BytesIO, InlineKeyboardMarkup]:
    path = pathlib.Path("resources") / "emojis"

    all_emoji = random.sample([x.stem for x in path.glob("*.png")], MAX_EMOJI)
    correct_emoji = random.sample(all_emoji, MAX_EMOJI_CORRECT)

    return get_image(correct_emoji, path), get_keyboard(
        all_emoji, correct_emoji, user_id
    )
