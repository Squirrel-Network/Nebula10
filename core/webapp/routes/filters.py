#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template, request

from core.database.repository import GroupRepository

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


@filters.route("/<group_id>", methods=["GET"])
def index(group_id: int):
    with GroupRepository() as db:
        data = db.get_by_id(group_id)

    if not data:
        return "Error!"

    print(request.args)

    return render_template(
        "filters/index.html",
        filters={k: v for k, v in data.items() if k in FILTERS_KEY},
    )
