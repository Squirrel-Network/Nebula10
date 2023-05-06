#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

__all__ = [
    "CommunityRepository",
    "DashboardRepository",
    "GroupRepository",
    "GroupLanguageRepository",
    "SuperbanRepository",
    "UserRepository",
]

from .community import CommunityRepository
from .dashboard import DashboardRepository
from .group import GroupRepository
from .group_language import GroupLanguageRepository
from .superban import SuperbanRepository
from .user import UserRepository
