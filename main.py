#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import logging
import sys

from dotenv import load_dotenv
from telegram.ext import Application

from config import Config, Session
from core.database import create_pool
from core.database.repository.user import UserRepository
from core.utilities.functions import get_owner_list
from languages import load_languages


# if version < 3.10, stop bot.
LOGGING = logging.getLogger(__name__)
if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    LOGGING.error("You MUST have a python version of at least 3.10! Multiple features depend on this. Bot quitting.")
    quit(1)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    # Load .env file
    load_dotenv()

    # Load the Config
    conf = Session.config = Config()

    # Load pool
    Session.db_pool = create_pool()

    # Load languages
    Session.lang = load_languages()

    # Add owner
    UserRepository().add_owner(conf.OWNER_ID, conf.OWNER_USERNAME.lower())

    # Get owner ids
    Session.owner_ids = get_owner_list()

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(conf.BOT_TOKEN).build()

    # on different commands - answer in Telegram
    from core.commands import commands_index
    commands_index.user_command(application)
    commands_index.admin_command(application)
    commands_index.owner_command(application)

    # Handlers
    from core.handlers import handlers_index
    handlers_index.core_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()