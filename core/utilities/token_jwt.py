#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import datetime

import jwt

from config import Session


def encode_jwt() -> str:
    payload = dict(
        exp=datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(seconds=Session.config.JWT_TOKEN_EXPIRES)
    )

    return jwt.encode(payload, Session.config.TOKEN_SECRET, algorithm="HS256")
