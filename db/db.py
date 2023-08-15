import psycopg2
from config.config import HOST, PORT, DBNAME, PASSWORD, USER

from utils.logging import logging
from psycopg2 import sql



class PgConn:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            # print(error)
            logging.error(error)

# User section
    def update_user(self, user_id, firstname, lastname, role, email, soc_link, about):
        with self.conn:
            self.cur.execute("UPDATE users SET firstname = %s, lastname = %s, "
                             "role = %s, email = %s, soc_link = %s, about = %s WHERE tg_id = %s;",
                             (firstname, lastname, role, email, soc_link, about, user_id))
            self.conn.commit()

    def update_state(self, user_id, text):
        with self.conn:
            self.cur.execute("UPDATE users SET state = %s WHERE tg_id = %s;", (text, user_id))
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

    def get_user_lang(self, user_id):
        with self.conn:
            self.cur.execute("SELECT lang FROM users WHERE tg_id = %s;", (user_id,))
            return self.cur.fetchone()[0]

    def get_user_full_info(self, user_id):
        with self.conn:
            self.cur.execute("SELECT string_agg(f.name, ', ') FROM fields f "
                             "JOIN unnest((SELECT intersted_in FROM users WHERE tg_id = %s)) AS field_id "
                             "ON f.id = field_id;", (user_id,))
            # field_names = [row[0] for row in self.cur.fetchall()]
            interested_in = self.cur.fetchone()[0]
            interested_in = interested_in if interested_in is not None else ""

            self.cur.execute("SELECT string_agg(f.name, ', ') FROM fields f "
                             "JOIN unnest((SELECT work_with FROM users WHERE tg_id = %s)) AS field_id "
                             "ON f.id = field_id;", (user_id,))
            # field_names = [row[0] for row in self.cur.fetchall()]
            work_with = self.cur.fetchone()[0]
            work_with = work_with if work_with is not None else ""

            self.cur.execute("SELECT firstname, lastname, email, soc_link, role, about "
                             "FROM users WHERE tg_id = %s;", (user_id,))

            user_info = list(self.cur.fetchone())
            user_info.extend([interested_in, work_with])

            self.cur.execute("SELECT name, description "
                             "FROM startups WHERE user_id = (SELECT id FROM users WHERE tg_id = %s);", (user_id,))
            val = self.cur.fetchone()

            startup = val if val is not None else ['', '']

            user_info.extend(startup)

            return user_info

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

    def set_interested_in(self, user_id, field):
        with self.conn:
            # if type(field) == str:
            #     field = [field]
            self.cur.execute(" UPDATE users SET intersted_in = %s WHERE tg_id = %s; ", (field, user_id))
            self.conn.commit()

    def set_work_with(self, user_id, field):
        with self.conn:
            # if type(field) == str:
            #     field = [field]
            self.cur.execute(" UPDATE users SET work_with = %s WHERE tg_id = %s; ", (field, user_id))
            self.conn.commit()

    def add_fields(self, values):
        with self.conn:
            insert_values = [[val[0].strip().lower()] for val in values]

            self.cur.executemany("""INSERT INTO fields(name) VALUES(%s) ON CONFLICT(name) DO NOTHING""",
                                 insert_values)
            self.conn.commit()

            self.cur.execute(""" SELECT id FROM fields WHERE name IN %s """,
                             (tuple([val[0] for val in insert_values]), ))
            return [val[0] for val in self.cur.fetchall()]
