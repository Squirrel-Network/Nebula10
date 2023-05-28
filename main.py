#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import sys

from dotenv import load_dotenv
from loguru import logger
from telegram.ext import Application

from config import Config, Session
from core.callback_query import callback_query_index
from core.commands import commands_index
from core.database import create_pool
from core.database.repository import SuperbanRepository, UserRepository
from core.handlers import handlers_index
from core.utilities.functions import get_owner_list
from languages import load_languages

# if version < 3.10, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    logger.error(
        "You MUST have a python version of at least 3.10! Multiple features depend on this. Bot quitting."
    )
    quit(1)


FMT = "<green>[{time}]</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"


def main() -> None:
    # Configure loguru
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "format": FMT},
            {"sink": "file.log", "format": FMT},
        ]
    )

    logger.info("Application started")

    # Load .env file
    logger.info("Load .env file")
    load_dotenv()

    # Load the Config
    conf = Session.config = Config()

    # Load pool
    logger.info("Start database (pool)")
    Session.db_pool = create_pool()

    # Load languages
    logger.info("Load langueages")
    Session.lang = load_languages()

    # Add owner
    logger.info("Add owner in database if not exist")
    with UserRepository() as db:
        db.add_owner(conf.OWNER_ID, conf.OWNER_USERNAME.lower())

    with SuperbanRepository() as db:
        db.add_whitelist(conf.OWNER_ID, conf.OWNER_USERNAME.lower())

    # Get owner ids
    Session.owner_ids = get_owner_list()

    # Start the bot.
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(conf.BOT_TOKEN).build()

    # on different commands - answer in Telegram
    commands_index.user_command(application)
    commands_index.admin_command(application)
    commands_index.owner_command(application)
    callback_query_index.user_callback(application)
    callback_query_index.admin_callback(application)
    callback_query_index.owner_callback(application)

    # Handlers
    handlers_index.core_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
