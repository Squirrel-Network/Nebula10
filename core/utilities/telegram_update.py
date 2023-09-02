#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram import Chat, Update, User

from config import Session
from languages import get_group_lang, get_lang
from languages.lang import Lang, LangKeyboard


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

    @property
    async def lang(self) -> Lang:
        return await get_lang(self)

    @property
    async def lang_keyboard(self) -> LangKeyboard:
        lang = await get_group_lang(self.chat.id)

        return Session.lang_keyboard[f"{lang.lower()}_keyboard"]
