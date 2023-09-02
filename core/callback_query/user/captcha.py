#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Session
from core.database.models import Groups
from core.decorators import on_update
from core.handlers.chat_handlers.welcome import welcome_user
from core.utilities.functions import unmute_user
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang

MAX_MISTAKES = 3


@on_update()
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    _, position, mistakes, tot_correct, user_id = update.callback_query.data.split("|")

    if int(user_id) != update.effective_user.id:
        return await update.callback_query.answer(lang["WELCOME_CAPTCHA_ERROR_USER_ID"])

    key = f"{update.effective_user.id}-{update.effective_chat.id}"

    if not key in Session.captcha:
        return await update.callback_query.answer(lang["WELCOME_CAPTCHA_NOT_VALID"])

    correct = int(position) in Session.captcha[key]["correct_position"]

    if correct:
        tot_correct = int(tot_correct) + 1
    else:
        mistakes = int(mistakes) + 1

    if mistakes == MAX_MISTAKES:
        del Session.captcha[key]

        await update.effective_message.delete()
        return await message(update, context, lang["WELCOME_CAPTCHA_NOT_RESOLVE"])

    if tot_correct == 6:
        del Session.captcha[key]

        await update.effective_message.delete()
        await unmute_user(update.effective_chat.id, user_id, context)

        group_data = await Groups.get(id_group=update.effective_chat.id)

        return await welcome_user(
            update, context, update.effective_user, group_data.welcome_text
        )

    keyboard = [
        [
            InlineKeyboardButton(
                "{CHECK_MARK_BUTTON}".format_map(Text())
                if correct
                else "{CROSS_MARK}".format_map(Text()),
                callback_data="XX",
            )
            if y.callback_data == update.callback_query.data
            else InlineKeyboardButton(
                y.text,
                callback_data=f"captcha|{y.callback_data.split('|')[1]}|{mistakes}|{tot_correct}|{user_id}"
                if "captcha" in y.callback_data
                else y.callback_data,
            )
            for y in x
        ]
        for x in update.effective_message.reply_markup.inline_keyboard
    ]

    await update.callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(keyboard)
    )
