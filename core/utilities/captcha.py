#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import io
import pathlib
import random
import time

from PIL import Image
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.utilities import emoji
from core.utilities.functions import mute_user
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text

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


def get_keyboard(all_emoji: list[str], user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        InlineKeyboardButton(
            getattr(emoji, x),
            callback_data=f"captcha|{i}|0|0|{user_id}",
        )
        for i, x in enumerate(all_emoji)
    ]

    return InlineKeyboardMarkup(build_menu(keyboard, 5))


async def get_catcha(
    update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE, lang: dict
):
    path = pathlib.Path("resources") / "emojis"
    user = update.effective_user
    chat_id = update.effective_chat.id

    key = f"{user.id}-{chat_id}"
    all_emoji = random.sample([x.stem for x in path.glob("*.png")], MAX_EMOJI)
    correct_emoji = random.sample(all_emoji, MAX_EMOJI_CORRECT)
    correct_position = [all_emoji.index(x) for x in correct_emoji]

    Session.captcha[key]["correct_position"] = correct_position
    Session.captcha[key]["username"] = user.username
    Session.captcha[key]["time"] = time.monotonic()

    await mute_user(chat_id, user.id, context)
    image, keyboard = get_image(correct_emoji, path), get_keyboard(all_emoji, user.id)

    m = await message(
        update,
        context,
        lang["WELCOME_CAPTCHA"].format_map(Text()),
        type="photo",
        reply_markup=keyboard,
        img=image,
    )

    Session.captcha[key]["message_id"] = m.message_id
