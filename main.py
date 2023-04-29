#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import logging
import sys

from telegram.ext import Application

from core.config import Session


# if version < 3.7, stop bot.
LOGGING = logging.getLogger(__name__)
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGING.error("You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting.")
    quit(1)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Session.config.BOT_TOKEN).build()
    bot = application.add_handler

    # on different commands - answer in Telegram
    from core.commands import commands_index

    commands_index.user_command(bot)
    commands_index.admin_command(bot)
    commands_index.owner_command(bot)

    # Handlers
    from core.handlers import handlers_index

    handlers_index.core_handlers(bot)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()