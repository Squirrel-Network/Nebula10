#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template

from core.database.repository import GroupRepository
from core.utilities.token_jwt import TokenJwt
from core.webapp.utils.auth import auth_required

FILTERS_KEY = [
    GroupRepository.EXE_FILTER,
    GroupRepository.GIF_FILTER,
    GroupRepository.ZIP_FILTER,
    GroupRepository.TARGZ_FILTER,
    GroupRepository.JPG_FILTER,
    GroupRepository.DOCX_FILTER,
    GroupRepository.APK_FILTER,
]
filters = Blueprint("filters", __name__)


@filters.route("/<token>", methods=["GET"])
@auth_required
def index(token: TokenJwt):
    with GroupRepository() as db:
        data = db.get_by_id(token.group_id)

    if not data:
        return "Error!"

    return render_template(
        "filters/index.html",
        filters={k: v for k, v in data.items() if k in FILTERS_KEY},
    )
