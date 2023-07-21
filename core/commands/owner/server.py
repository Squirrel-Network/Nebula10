#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime
import platform

import psutil
from telegram import constants
from telegram.ext import ContextTypes

from core.decorators import delete_command, on_update
from core.utilities import filters
from core.utilities.enums import Role
from core.utilities.telegram_update import TelegramUpdate
from core.utilities.text import Text
from languages import get_lang


def get_size(num_bytes: int, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if num_bytes < factor:
            return f"{num_bytes:.2f}{unit}{suffix}"
        num_bytes /= factor


async def get_message(update: TelegramUpdate) -> str:
    lang = await get_lang(update)
    uname = platform.uname()
    net_io = psutil.net_io_counters()

    msg = lang["SERVER_STATUS_SYSTEM"].format_map(
        Text(
            {
                "system": uname.system,
                "node": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
            }
        )
    )
    msg += lang["SERVER_STATUS_CPU"].format_map(
        Text(
            {
                "cpu_percent": psutil.cpu_percent(),
                "cpu_freq": psutil.cpu_freq().current,
                "core": psutil.cpu_count(logical=False),
                "core_logic": psutil.cpu_count(logical=True),
            }
        )
    )
    msg += lang["SERVER_STATUS_DISK_MESSAGE"].format_map(Text())

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        msg += lang["SERVER_STATUS_DISK"].format_map(
            Text(
                {
                    "total": get_size(partition_usage.total),
                    "used": get_size(partition_usage.used),
                    "free": get_size(partition_usage.free),
                    "percent": partition_usage.percent,
                }
            )
        )

    msg += lang["SERVER_STATUS_MEMORY"].format_map(
        Text(
            {
                "memory_percent": psutil.virtual_memory()[2],
                "total": get_size(psutil.virtual_memory().total),
            }
        )
    )
    msg += lang["SERVER_STATUS_NETWORK"].format_map(
        Text(
            {
                "bytes_sent": get_size(net_io.bytes_sent),
                "bytes_recv": get_size(net_io.bytes_recv),
                "running": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
                    "%A %d. %B %Y"
                ),
            }
        )
    )

    return msg


@on_update(filters=filters.command(["server"]) & filters.check_role(Role.OWNER))
@delete_command
async def init(update: TelegramUpdate, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        update.effective_chat.id,
        await get_message(update),
        parse_mode=constants.ParseMode.HTML,
    )
