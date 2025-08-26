from flask_login import UserMixin
import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db():
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    return con

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE google_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return User(id=row["google_id"], username=row["username"])
        return None
