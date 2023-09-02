#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InlineKeyboardMarkup, Message, Update, constants
from telegram.ext import ContextTypes


async def message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str | None = None,
    parse: str = constants.ParseMode.HTML,
    type: str = "message",
    chat_id: int | str | None = None,
    img: str = None,
    reply_markup: InlineKeyboardMarkup = None,
    allow_sending_without_reply: bool | None = None,
) -> Message:
    bot = context.bot
    chat = update.effective_chat
    thread_id = (
        update.effective_message.message_thread_id
        if (
            update.effective_message
            and update.effective_message.message_thread_id
            and update.effective_message.is_topic_message
        )
        else None
    )

    match type:
        case "message":
            return await bot.send_message(
                chat.id,
                text,
                parse_mode=parse,
                message_thread_id=thread_id,
                reply_markup=reply_markup,
                allow_sending_without_reply=allow_sending_without_reply,
            )

        case "photo":
            return await bot.sendPhoto(
                chat_id=update.effective_chat.id,
                photo=img,
                caption=text,
                parse_mode=parse,
                message_thread_id=thread_id,
                reply_markup=reply_markup,
            )

        case "reply":
            return await update.message.reply_text(
                text,
                parse_mode=parse,
                message_thread_id=thread_id,
                reply_markup=reply_markup,
            )

        case "messageid":
            return await bot.send_message(chat_id, text, parse_mode=parse)

        case "private":
            return await bot.send_message(
                update.message.from_user.id,
                text,
                parse_mode=parse,
                reply_markup=reply_markup,
            )

        case "animation":
            return await bot.sendAnimation(
                chat.id, img, caption=text, message_thread_id=thread_id
            )
