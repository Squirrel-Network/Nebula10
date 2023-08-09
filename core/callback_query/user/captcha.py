#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database.models import Groups
from core.decorators import on_update
from core.handlers.chat_handlers.welcome import welcome_user
from core.utilities.captcha import decrypt_data, encrypt_data
from core.utilities.functions import unmute_user
from core.utilities.menu import build_menu
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

MAX_MISTAKES = 3


@on_update()
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    data = update.callback_query.data
    correct, mistakes, tot_correct, user_id = decrypt_data(data.split("|")[1])

    if user_id != update.effective_user.id:
        return await update.callback_query.answer(lang["WELCOME_CAPTCHA_ERROR_USER_ID"])

    if correct:
        tot_correct += 1
    else:
        mistakes += 1

    if mistakes == MAX_MISTAKES:
        await update.effective_message.delete()
        return await message(update, context, lang["WELCOME_CAPTCHA_NOT_RESOLVE"])

    if tot_correct == 6:
        await unmute_user(update.effective_chat.id, user_id, context)

        group_data = await Groups.get(id_group=update.effective_chat.id).values()

        await update.effective_message.delete()
        return await welcome_user(update, context, update.effective_user, group_data)

    keyboard = []

    for x in update.effective_message.reply_markup.inline_keyboard:
        for y in x:
            c, _, _, _ = decrypt_data(y.callback_data.replace("captcha|", ""))

            keyboard.append(
                InlineKeyboardButton(
                    y.text
                    if not data == y.callback_data
                    else "{CHECK_MARK_BUTTON}".format_map(Text())
                    if correct
                    else "{CROSS_MARK}".format_map(Text()),
                    callback_data=f"captcha|{encrypt_data(c, mistakes, tot_correct, user_id)}",
                )
            )

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(build_menu(keyboard, 5))
    )
