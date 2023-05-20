#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from core.database.db_connect import Connection


class GroupRepository(Connection):
    ###### Column constants of the table ######
    SET_ID_GROUP = "id_group"
    SET_GROUP_NAME = "group_name"
    SET_WELCOME_TEXT = "welcome_text"
    SET_WELCOME_BUTTONS = "welcome_buttons"
    SET_RULES_TEXT = "rules_text"
    SET_COMMUNITY = "community"
    SET_LANGUAGE = "languages"
    SET_WELCOME = "set_welcome"
    SET_MAX_WARN = "max_warn"
    SET_SILENCE = "set_silence"
    EXE_FILTER = "exe_filter"
    SET_BLOCK_N_M = "block_new_member"
    SET_ARABIC = "set_arabic_filter"
    SET_CIRILLIC = "set_cirillic_filter"
    SET_CHINESE = "set_chinese_filter"
    SET_USER_PROFILE_PICT = "set_user_profile_picture"
    GIF_FILTER = "gif_filter"
    SET_CAS_BAN = "set_cas_ban"
    SET_TPNU = "type_no_username"
    SET_LOG_CHANNEL = "log_channel"
    SET_GROUP_PHOTO = "group_photo"
    SET_GROUP_MEMBERS_COUNT = "total_users"
    ZIP_FILTER = "zip_filter"
    TARGZ_FILTER = "targz_filter"
    JPG_FILTER = "jpg_filter"
    DOCX_FILTER = "docx_filter"
    APK_FILTER = "apk_filter"
    ZOOPHILE_FILTER = "zoophile_filter"
    SENDER_CHAT_BLOCK = "sender_chat_block"
    SPOILER_BLOCK = "spoiler_block"
    SET_NO_VOCAL = "set_no_vocal"
    SET_ANTIFLOOD = "set_antiflood"
    BAN_MESSAGE = "ban_message"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    SET_GH = "set_gh"

    def get_by_id(self, chat_id: int):
        q = "SELECT * FROM groups WHERE id_group='%s'"

        return self._select(q, (chat_id,))

    def get_all(self):
        q = "SELECT * FROM groups"

        return self._select_all(q)

    # Save group by Welcome
    def add_with_dict(self, dictionary: dict):
        placeholders = ", ".join(["%s"] * len(dictionary))
        columns = ", ".join(dictionary.keys())
        q = "INSERT INTO groups ( %s ) VALUES ( %s )" % (columns, placeholders)

        return self._dict_insert(q, dictionary)

    # Update welcome buttons
    def updateWelcomeButtonsByGroupId(self, group_id: int, button: str):
        q = "UPDATE `groups` SET `welcome_buttons`=%s WHERE `id_group`=%s"

        self._execute(q, (button, group_id))

    # I update the group id if the group changes from group to supergroup
    def update(self, back_id_group: int, id_group: int):
        q = "UPDATE groups SET id_group = %s WHERE id_group = %s"
        return self._execute(q, (back_id_group, id_group))

    # I insert the updates for the message count by group
    def insert_updates(self, data: list[tuple]):
        q = "INSERT INTO nebula_updates (update_id, message_id, tg_group_id, tg_user_id, date) VALUES (%s,%s,%s,%s,%s)"
        return self._execute_many(q, data)

    # I collect the updates to know how many messages have been sent
    def get_updates_by_chat_month(self, group_id: int):
        q = "SELECT COUNT(*) AS counter FROM nebula_updates WHERE date BETWEEN DATE_SUB(NOW(), INTERVAL 31 DAY) AND NOW() AND tg_group_id = %s ORDER BY date DESC"

        return self._select(q, (group_id,))

    def get_updates_by_user_month(self, group_id: int, user_id: int):
        q = "SELECT COUNT(*) AS counter FROM nebula_updates WHERE DATE BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() AND tg_group_id = %s AND tg_user_id = %s ORDER BY DATE DESC"

        return self._select(q, (group_id, user_id))

    def get_all_updates(self):
        q = "SELECT COUNT(*) AS counter FROM nebula_updates"

        return self._select(q)

    def change_group_photo(self, group_id: int, group_photo: str):
        q = "INSERT INTO groups SET group_photo = %s WHERE id_group = %s"

        return self._execute(q, (group_photo, group_id))

    def get_group_badwords(self, group_id: int, word: str):
        q = "SELECT * FROM groups_badwords WHERE INSTR(%s, word) <> 0 AND tg_group_id = %s"

        return self._select(q, (word, group_id))

    def get_antispam_logic(self, logic: str):
        q = "SELECT logic FROM nebula_antispam WHERE INSTR(%s, logic) <> 0"

        return self._select(q, (logic,))

    def get_badwords_group(self, group_id: int):
        q = "SELECT * FROM groups_badwords WHERE tg_group_id = %s"

        return self._select_all(q, (group_id,))

    def insert_badword(self, word: str, group_id: int):
        q = "INSERT IGNORE INTO groups_badwords (word, tg_group_id) VALUES (%s,%s)"

        return self._execute(q, (word, group_id))

    def insert_spam(self, logic: str):
        q = "INSERT IGNORE INTO nebula_antispam (logic) VALUES (%s)"

        return self._execute(q, (logic,))

    def remove(self, group_id: int):
        q = "DELETE FROM groups WHERE id_group = %s"
        return self._execute(q, (group_id,))

    def get_custom_handler(self, question: str, chat_id: int):
        q = "SELECT answer FROM custom_handler WHERE question = %s AND chat_id = %s"

        return self._select(q, (question, chat_id))

    def insert_custom_handler(self, chat_id: int, question: str, answer: str):
        q = "INSERT INTO custom_handler (chat_id, question, answer) VALUES (%s,%s,%s)"

        return self._execute(q, (chat_id, question, answer))

    def get_top_active_users(self, group_id: int):
        q = "SELECT COUNT(*) AS counter, u.tg_username, u.tg_id FROM nebula_updates nu INNER JOIN users u ON u.tg_id = nu.tg_user_id WHERE DATE BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() AND nu.tg_group_id = %s GROUP BY nu.tg_user_id ORDER BY counter DESC LIMIT 10"

        return self._select_all(q, (group_id,))

    def get_top_inactive_users(self, group_id: int):
        q = "SELECT COUNT(*) AS counter, u.tg_username, u.tg_id FROM nebula_updates nu INNER JOIN users u ON u.tg_id = nu.tg_user_id WHERE DATE BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() AND nu.tg_group_id = %s GROUP BY nu.tg_user_id ORDER BY counter ASC LIMIT 10"

        return self._select_all(q, (group_id,))

    # GROUP SETTINGS
    def update_group_settings(self, record: str, value: str, group_id: int):
        q = "UPDATE groups SET @record = %s WHERE id_group = %s".replace(
            "@record", record
        )
        print(q)

        return self._execute(q, (value, group_id))

    def job_nebula_updates(self):
        q = "DELETE FROM nebula_updates WHERE date < NOW() - INTERVAL 90 DAY"

        return self._execute(q)
