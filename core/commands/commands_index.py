#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import Application, MessageHandler

from core.commands import admin, owner, user


def admin_command(application: Application):
    application.add_handler(MessageHandler(None, admin.filters.init))
    application.add_handler(MessageHandler(None, admin.say.init))
    application.add_handler(MessageHandler(None, admin.settings.init))
    application.add_handler(MessageHandler(None, admin.usearch.init))
    application.add_handler(MessageHandler(None, admin.ban.init))
    application.add_handler(MessageHandler(None, admin.ban.init_reply))
    application.add_handler(
        MessageHandler(
            None,
            admin.ban.set_ban_message,
        )
    )
    application.add_handler(
        MessageHandler(
            None,
            admin.ban.set_ban_message_reply,
        )
    )
    application.add_handler(MessageHandler(None, admin.unban.init_reply))
    application.add_handler(MessageHandler(None, admin.check_permission.init))
    application.add_handler(MessageHandler(None, admin.warn.init_reply))
    application.add_handler(MessageHandler(None, admin.warn.set_max_warn))
    application.add_handler(MessageHandler(None, admin.antiflood.set_antiflood))
    application.add_handler(MessageHandler(None, admin.antistorm.set_antistorm))
    application.add_handler(MessageHandler(None, admin.set_welcome.set_welcome))
    application.add_handler(MessageHandler(None, admin.set_welcome.set_welcome_reply))
    application.add_handler(MessageHandler(None, admin.set_rules.set_rules))
    application.add_handler(
        MessageHandler(None, admin.set_welcome_buttons.set_welcome_buttons)
    )
    application.add_handler(
        MessageHandler(None, admin.set_welcome_buttons.add_button_status)
    )
    application.add_handler(MessageHandler(None, admin.info_group.init))
    application.add_handler(MessageHandler(None, admin.info_group.chat_id))
    application.add_handler(MessageHandler(None, admin.pin.init))
    application.add_handler(MessageHandler(None, admin.pin.get_pinned))
    application.add_handler(MessageHandler(None, admin.pin.unpin))


def owner_command(application: Application):
    application.add_handler(MessageHandler(None, owner.test.command_test))
    application.add_handler(MessageHandler(None, owner.server.init))
    application.add_handler(MessageHandler(None, owner.superban.init))
    application.add_handler(MessageHandler(None, owner.superban.multi_superban))
    application.add_handler(MessageHandler(None, owner.superban.remove_superban_via_id))
    application.add_handler(MessageHandler(None, owner.add_owner.init))
    application.add_handler(MessageHandler(None, owner.add_community.init))


def user_command(application: Application):
    application.add_handler(MessageHandler(None, user.start.init))
    application.add_handler(MessageHandler(None, user.io.init))
    application.add_handler(MessageHandler(None, user.help_command.init))
    application.add_handler(MessageHandler(None, user.rules.rules))
    application.add_handler(MessageHandler(None, user.report.report))
    application.add_handler(MessageHandler(None, user.eggs.lost_command))
    application.add_handler(MessageHandler(None, user.eggs.fiko_command))
    application.add_handler(MessageHandler(None, user.eggs.nanachi_command))
    application.add_handler(MessageHandler(None, user.kickme.kickme_command))
