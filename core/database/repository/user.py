#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class UserRepository(Connection):
    def get_by_id(self, user_id):
        q = "SELECT * FROM users WHERE tg_id='%s'"

        return self._select(q, (user_id,))

    def get_by_username(self, username: str):
        q = "SELECT * FROM users WHERE tg_username = %s"

        return self._select(q, (username,))

    def get_user_by_group(self, user_id: int, group_id: int):
        q = "SELECT u.tg_id,u.tg_username,gr.id_group,gu.warn_count, gr.max_warn, gr.group_name FROM users u INNER JOIN group_users gu ON gu.tg_id = u.tg_id INNER JOIN groups gr ON gu.tg_group_id = gr.id_group WHERE u.tg_id = %s AND gr.id_group = %s"

        return self._select(q, (user_id, group_id))

    def get_user_by_groups(self, user_id: int):
        q = "SELECT u.tg_id,u.tg_username,gr.id_group,gu.warn_count, gr.max_warn, gr.group_name FROM users u INNER JOIN group_users gu ON gu.tg_id = u.tg_id INNER JOIN groups gr ON gu.tg_group_id = gr.id_group WHERE u.tg_id = %s"

        return self._select_all(q, (user_id,))

    def get_all(self, user_id: int):
        q = "SELECT * FROM users WHERE tg_id='%s'"

        return self._select_all(q, (user_id,))

    def add(self, user_id: int, username: str, created_at: str, updated_at: str):
        q = "INSERT IGNORE INTO users (tg_id, tg_username, created_at, updated_at) VALUES (%s,%s,%s,%s)"

        return self._execute(q, (user_id, username, created_at, updated_at))

    def add_owner(self, user_id: int, username: str):
        q = "INSERT IGNORE INTO owner_list (tg_id, tg_username) VALUES (%s,%s)"

        return self._execute(q, (user_id, username))

    def remove_owner(self, user_id: int):
        q = "DELETE FROM owner_list WHERE tg_id = %s"

        return self._execute(q, (user_id,))

    def add_into_mtm(
        self, user_id: int, group_id: int, warn_count: int, user_score: int
    ):
        q = "INSERT IGNORE INTO group_users (tg_id, tg_group_id, warn_count, user_score) VALUES (%s,%s,%s,%s)"

        return self._execute(q, (user_id, group_id, warn_count, user_score))

    def update(self, username: str, updated_at, user_id: int):
        q = "UPDATE users SET tg_username = %s, updated_at = %s WHERE tg_id = %s"

        return self._execute(q, (username, updated_at, user_id))

    def delete_user(self, user_id: int):
        q = "DELETE FROM users WHERE tg_id = %s"

        return self._execute(q, (user_id,))

    def update_warn(self, user_id: int, group_id: int):
        q = "UPDATE group_users SET warn_count = warn_count + 1 WHERE tg_id = %s AND tg_group_id = %s"

        return self._execute(q, (user_id, group_id))

    def down_warn(self, user_id: int, group_id: int):
        q = "UPDATE group_users SET warn_count = warn_count - 1 WHERE tg_id = %s AND tg_group_id = %s"

        return self._execute(q, (user_id, group_id))

    def remove_warn(self, user_id: int, group_id: int):
        q = "UPDATE group_users SET warn_count = 0 WHERE tg_id = %s AND tg_group_id = %s"

        return self._execute(q, (user_id, group_id))

    def get_owners(self):
        q = "SELECT * FROM owner_list"

        return self._select_all(q)

    def get_owner_by_id(self, user_id: int):
        q = "SELECT * FROM owner_list WHERE tg_id='%s'"

        return self._select(q, (user_id,))

    def get_linktree_main_text(self, user_id: int):
        q = "SELECT * FROM linktree_main_text WHERE user_id='%s'"

        return self._select(q, (user_id,))

    def get_link_tree_buttons(self, user_id: int):
        q = "SELECT * FROM linktree_buttons WHERE user_id='%s'"

        return self._select_all(q, (user_id,))

    def insert_linktree_button(
        self, user_id: int, button_text: str, button_url: str
    ):
        q = "INSERT INTO linktree_buttons (user_id, button_id, button_text, button_url) VALUES (%s, NULL, %s, %s)"

        return self._execute(q, (user_id, button_text, button_url))

    def insert_main_text_linktree(self, user_id: int, main_text: str):
        q = "INSERT INTO linktree_main_text (user_id, main_text) VALUES (%s,%s)"

        return self._execute(q, (user_id, main_text))

    def update_main_text_linktree(self, main_text: str, user_id: int):
        q = "UPDATE linktree_main_text SET main_text = %s WHERE user_id = %s"

        return self._update(q, (main_text, user_id))

    def delete_linktree_button(self, button_id: int, user_id: int):
        q = "DELETE FROM linktree_buttons WHERE button_id = %s AND user_id = %s"

        return self._execute(q, (button_id, user_id))
