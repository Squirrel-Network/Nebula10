#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from telegram.ext import ContextTypes

from core.database.models import GroupsFilters
from core.decorators import on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.message import message
from core.utilities.telegram_update import TelegramUpdate
from languages import get_lang

DOCUMENT_DATA = (
    (
        ("application/vnd.android.package-archive",),
        "apk_filter",
        "AUTOMATIC_FILTER_HANDLER_APK",
    ),
    (
        (
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "docx_filter",
        "AUTOMATIC_FILTER_HANDLER_DOCX",
    ),
    (
        ("application/x-ms-dos-executable",),
        "exe_filter",
        "AUTOMATIC_FILTER_HANDLER_EXE",
    ),
    (("video/mp4",), "gif_filter", "AUTOMATIC_FILTER_HANDLER_GIF"),
    (("image/jpeg",), "jpg_filter", "AUTOMATIC_FILTER_HANDLER_JPG"),
    (
        ("application/x-compressed-tar", "application/zip"),
        "compress_filter",
        "AUTOMATIC_FILTER_HANDLER_ZIP_TARGZ",
    ),
)


@on_update(
    True,
    filters.group
    & filters.document
    & ~filters.check_role(Role.ADMINISTRATOR, Role.CREATOR, Role.OWNER),
)
async def filters_chat(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    lang = await get_lang(update)
    mime_type = update.effective_message.document.mime_type
    data = await GroupsFilters.get(chat_id=update.effective_chat.id).values()

    for mime_types, db, msg in DOCUMENT_DATA:
        if mime_type in mime_types and data[db]:
            await update.effective_message.delete()
            await message(update, context, lang[msg])
