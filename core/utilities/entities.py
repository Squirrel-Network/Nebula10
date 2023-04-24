#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

class TelegramObjects:
    def __init__(self, update, context):
        self.bot = context.bot
        self.chat = update.effective_chat
        self.user = update.effective_message.from_user
        self.user_reply = update.message.reply_to_message.from_user if update.message.reply_to_message else None
        self.new_user = next(iter(update.message.new_chat_members), None)

    def chat_object(self):
        chat = self.chat
        return chat

    def user_object(self):
        user = self.user
        return user

    def user_reply_object(self):
        user = self.user_reply
        return user

    def new_user_object(self):
        user = self.new_user
        return user
    def bot_object(self):
        bot = self.bot
        return bot
