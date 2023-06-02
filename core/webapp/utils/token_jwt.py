#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import dataclasses
import datetime

import jwt
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidIssuedAtError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)

from config import Session


@dataclasses.dataclass
class TokenJwt:
    user_id: int
    group_id: int
    exp: int

    def to_dict(self):
        return dict(user_id=self.user_id, group_id=self.group_id, exp=self.exp)


def encode_jwt(payload: TokenJwt) -> str:
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(seconds=Session.config.JWT_TOKEN_EXPIRES)

    return jwt.encode(payload.to_dict(), Session.config.TOKEN_SECRET, algorithm="HS256")


def decode_jwt(token: str) -> TokenJwt | None:
    try:
        result = jwt.decode(token, Session.config.TOKEN_SECRET, algorithms=["HS256"])

        return TokenJwt(**result)
    except (
        InvalidTokenError,
        DecodeError,
        InvalidSignatureError,
        ExpiredSignatureError,
        InvalidIssuedAtError,
        InvalidKeyError,
        InvalidAlgorithmError,
        MissingRequiredClaimError,
    ):
        return None
