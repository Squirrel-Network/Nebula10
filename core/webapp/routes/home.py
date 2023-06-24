#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from quart import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/", methods=["GET"])
async def index():
    return await render_template("home/index.html")
