#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class DashboardRepository(Connection):
    def get_by_id(self, user_id: int):
        q = "SELECT * FROM nebula_dashboard WHERE tg_id='%s'"

        return self._select(q, (user_id,))

    def get_by_group_id(self, group_id: int):
        q = "SELECT * FROM nebula_dashboard WHERE tg_group_id='%s'"

        return self._select(q, (group_id,))

    def get_by_username(self, username: str):
        q = "SELECT * FROM nebula_dashboard WHERE tg_username = %s"

        return self._select(q, (username,))

    def get_user_and_group(self, group_id: int, user_id: int):
        q = "SELECT * FROM nebula_dashboard WHERE tg_group_id = %s AND tg_id = %s"

        return self._select(q, (group_id, user_id))

    def add(
        self,
        user_id: int,
        username: str,
        group_id: int,
        enable: int,
        role: str,
        created_at,
        updated_at,
    ):
        q = "INSERT INTO nebula_dashboard (tg_id, tg_username, tg_group_id, enable, role, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        return self._execute(
            q,
            (
                user_id,
                username,
                group_id,
                enable,
                role,
                created_at,
                updated_at,
            ),
        )

    def update(
        self, username: str, role: str, updated_at, user_id: int, group_id: int
    ):
        q = "UPDATE nebula_dashboard SET tg_username = %s, role = %s, updated_at = %s WHERE tg_id = %s AND tg_group_id = %s"

        return self._execute(
            q, (username, role, updated_at, user_id, group_id)
        )
