#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import constants
from core.utilities.entities import TelegramObjects


async def message(
    update,
    context,
    text="",
    parse=constants.ParseMode.HTML,
    type="message",
    chat_id=None,
    img=None,
    reply_markup=None,
    allow_sending_without_reply=None,
):
    bot = context.bot
    chat = TelegramObjects(update, context).chat_object()
    thread_id = (
        update.effective_message.message_thread_id
        if (
            update.effective_message.message_thread_id
            and update.effective_message.is_topic_message
        )
        else None
    )

    if type == "message":
        send = await bot.send_message(
            chat.id,
            text,
            parse_mode=parse,
            message_thread_id=thread_id,
            reply_markup=reply_markup,
            allow_sending_without_reply=allow_sending_without_reply,
        )
    elif type == "photo":
        send = await bot.sendPhoto(
            chat_id=update.effective_chat.id,
            photo=img,
            caption=text,
            parse_mode=parse,
            message_thread_id=thread_id,
        )
    elif type == "reply":
        send = await update.message.reply_text(
            text,
            parse_mode=parse,
            message_thread_id=thread_id,
            reply_markup=reply_markup,
        )
    elif type == "messageid":
        send = await bot.send_message(chat_id, text, parse_mode=parse)
    elif type == "private":
        send = await bot.send_message(
            update.message.from_user.id,
            text,
            parse_mode=parse,
            reply_markup=reply_markup,
        )
    elif type == "animation":
        send = await bot.sendAnimation(
            chat.id, img, caption=text, message_thread_id=thread_id
        )
    return send
