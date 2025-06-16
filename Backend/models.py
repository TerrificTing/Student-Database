# backend/models.py
from flask_login import UserMixin
from flask import g
import sqlite3

def get_db():
    con = sqlite3.connect("student-database.db")
    con.row_factory = sqlite3.Row
    return con

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @classmethod
    def get(cls, google_id):
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        user_data = cur.fetchone()
        if user_data:
            return cls(user_data["google_id"], user_data["username"])
        return None

    @classmethod
    def create(cls, google_id, username):
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO users (google_id, username) VALUES (?, ?)", (google_id, username))
        con.commit()
        return cls(google_id, username)
