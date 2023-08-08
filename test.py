from db.db import PgConn

db_conn = PgConn()

print(db_conn.add_fields([['IT'], ['Food']]))

print(db_conn.add_fields([["Medicine"]]))