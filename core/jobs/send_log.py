#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import InputFile

from config import Session


# This function sends the log file to the Telegram log channel
# async def send_log(context: ContextTypes.DEFAULT_TYPE):
async def send_log():
    with open("file.log", "rb") as f:
        data = f.read()

    await Session.bot.send_document(
        Session.config.DEFAULT_DEBUG_CHANNEL, InputFile(data), "#log"
    )
