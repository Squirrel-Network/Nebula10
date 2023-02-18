#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

async def help_command(update, context) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")