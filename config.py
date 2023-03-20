#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    BOT_TOKEN = os.environ.get('TOKEN')