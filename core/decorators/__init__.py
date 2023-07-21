#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

__all__ = (
    "check_is_admin",
    "delete_command",
    "on_update",
    "check_role",
)


from .check_bot import check_is_admin
from .delete import delete_command
from .on_update import on_update
from .restricted import check_role
