#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class SuperbanRepository(Connection):
    def get_by_id(self, user_id: int):
        q = "SELECT * FROM superban_table WHERE user_id=%s"

        return self._select(q, (user_id,))

    def get_whitelist_by_id(self, user_id: int):
        q = "SELECT * FROM whitelist_table WHERE tg_id=%s"

        return self._select(q, (user_id,))

    def get_group_blacklist_by_id(self, group_id: int):
        q = "SELECT * FROM groups_blacklist WHERE tg_id_group=%s"

        return self._select(q, (group_id,))

    def add_whitelist(self, user_id: int, user_username: str):
        q = "INSERT IGNORE INTO whitelist_table(tg_id, tg_username) VALUES (%s,%s)"

        return self._execute(q, (user_id, user_username))

    def get_all(self, user_id: int):
        q = "SELECT user_id FROM superban_table WHERE user_id=%s"

        return self._select_all(q, (user_id,))

    def add(
        self,
        user_id: int,
        user_first_name: str,
        motivation_text: str,
        user_date: str,
        id_operator: int,
        username_operator: str,
        first_name_operator: str,
    ):
        q = "INSERT IGNORE INTO superban_table(user_id, user_first_name, motivation_text, user_date, id_operator, username_operator, first_name_operator) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        return self._execute(
            q,
            (
                user_id,
                user_first_name,
                motivation_text,
                user_date,
                id_operator,
                username_operator,
                first_name_operator,
            ),
        )

    def adds(self, params: list[tuple]):
        q = "INSERT IGNORE INTO superban_table(user_id, user_first_name, motivation_text, user_date, id_operator, username_operator, first_name_operator) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        return self._execute_many(q, params)

    def remove(self, user_id: int):
        q = "DELETE FROM superban_table WHERE user_id = %s"

        return self._execute(q, (user_id,))
