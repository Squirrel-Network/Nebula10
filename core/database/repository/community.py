#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class CommunityRepository(Connection):
    def get_all(self):
        q = "SELECT * FROM community"

        return self._select_all(q)

    def get_by_id(self, group_id: int):
        q = "SELECT * FROM community WHERE tg_group_id='%s'"

        return self._select(q, (group_id,))

    def update(self, group_name: str, group_id: str):
        q = "UPDATE community SET tg_group_name = %s WHERE tg_group_id = %s"

        return self._execute(q, (group_name, group_id))

    def add(
        self,
        group_name: str,
        group_id: int,
        group_link: str,
        language: str,
        type: str,
    ):
        q = "INSERT INTO community(tg_group_name, tg_group_id, tg_group_link, language, type) VALUES (%s,%s,%s,%s,%s)"

        return self._insert(q, (group_name, group_id, group_link, language, type))

    def get_community_groups(self):
        q = "SELECT * FROM community WHERE type = 'supergroup'"

        return self._select_all(q)

    def get_community_channels(self):
        q = "SELECT * FROM community WHERE type = 'channel'"

        return self._select_all(q)
