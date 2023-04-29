#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from dotenv import load_dotenv

from core.config import Config


# Load .env file
load_dotenv()


class Session:
    config: Config = Config()
