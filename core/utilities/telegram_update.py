#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Chat, Update, User


class TelegramUpdate(Update):
    @property
    def chat(self) -> Chat | None:
        return self.effective_chat

    @property
    def user(self) -> User | None:
        return self.effective_user

    @property
    def user_reply(self) -> User | None:
        return (
            self.message.reply_to_message.from_user
            if self.message.reply_to_message
            else None
        )
