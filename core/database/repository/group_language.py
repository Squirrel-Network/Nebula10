#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class GroupLanguageRepository(Connection):
    def get_by_id(self, group_id: int):
        q = "SELECT languages FROM groups WHERE id_group='%s'"

        return self._select(q, (group_id,))
