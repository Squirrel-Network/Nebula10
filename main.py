#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import logging
from config import Config
from core.commands import commands_index
from core.handlers import handlers_index
from telegram.ext import Application

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Config.BOT_TOKEN).build()
    bot = application.add_handler

    # on different commands - answer in Telegram es: /start
    commands_index.user_command(bot)
    commands_index.owner_command(bot)

    # Handlers
    handlers_index.core_handlers(bot)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()