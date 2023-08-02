import psycopg2
from psycopg2 import sql
from datetime import datetime
from config.config import HOST, PORT, DBNAME, PASSWORD, USER
import json
import pytz
import datetime
from datetime import timedelta
import random
# from utils.misc.logging import logging


class PgConn:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            print(error)
            # logging.error(error)

# User section
    def update_user(self, user_id, firstname, lastname, midname, role, email, phone, soc_link):
        with self.conn:
            self.cur.execute("UPDATE users SET firstname = %s, lastname = %s, midname = %s, "
                             "role = %s, email = %s, phone = %s, soc_link = %s WHERE tg_id = %s;",
                             (firstname, lastname, midname, role, email, phone, soc_link, user_id))
            self.conn.commit()

    def get_sec_code_time(self, code):
        with self.conn:
            self.cur.execute("SELECT sec_code_time, tg_id FROM users WHERE sec_code = %s;", (code, ))
            return self.cur.fetchone()

    def get_role_and_idtg(self, code):
        with self.conn:
            self.cur.execute("SELECT role, tg_id FROM users WHERE sec_code = %s;", (code, ))
            return self.cur.fetchone()

    def update_user_sec_info(self, user_id, sec_code_time):
        with self.conn:
            self.cur.execute("UPDATE users SET sec_code_time = %s WHERE tg_id = %s;",
                             (sec_code_time, user_id))
            self.conn.commit()

    def get_user_sec_info(self, user_id):
        with self.conn:
            self.cur.execute("SELECT sec_code, sec_code_time FROM users WHERE tg_id = %s;", (user_id,))
            return self.cur.fetchone()

    def add_startup(self, user_id, name, description):
        with self.conn:

            self.cur.execute("INSERT INTO startups(user_id, name, description) "
                             "VALUES((SELECT id FROM users WHERE tg_id = %s), %s, %s) "
                             "ON CONFLICT(user_id) DO UPDATE SET name = excluded.name, "
                             "description = excluded.description;", (user_id, name, description))
            self.conn.commit()

    def get_fields(self):
        with self.conn:
            self.cur.execute("SELECT id, name FROM fields ORDER BY id")

            fields = self.cur.fetchall()

            paired_fields = [[fields[i], fields[i + 1]] for i in range(0, len(fields), 2)]

            return paired_fields

    def set_field(self, user_id, field):
        with self.conn:
            if type(field) == str:
                field = [field]
            self.cur.execute("UPDATE users SET field = %s WHERE tg_id = %s;", (field, user_id))
            self.conn.commit()
