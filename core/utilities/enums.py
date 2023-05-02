#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import enum


class Role(str, enum.Enum):
    OWNER = "owner"
    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
