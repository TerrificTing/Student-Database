from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user
from requests.exceptions import HTTPError
from Backend.api.models import User, get_db
import os
from dotenv import load_dotenv

# Load .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

# Set up Google OAuth blueprint
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="google_auth"
)

@google_bp.route("/")
def login_index():
    return "Login via Google at /login/auth"

@google_bp.route("/auth", endpoint="google_auth")
def google_login():
    try:
        if not google.authorized:
            return redirect(url_for("google.login"))

        resp = google.get("/oauth2/v2/userinfo")
        resp.raise_for_status()
        user_info = resp.json()

        google_id = user_info.get("id")
        username = user_info.get("name")

        if not google_id:
            return "Failed to retrieve Google user ID", 400

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        user_row = cur.fetchone()

        if not user_row:
            cur.execute("INSERT INTO users (google_id, username) VALUES (?, ?)", (google_id, username))
            con.commit()

        user = User(id=google_id, username=username)
        login_user(user)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Internal Server Error: {e}", 500

    return redirect(url_for("dashboard"))

# Called on startup to ensure users table exists
def create_user_database():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            google_id TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)
    con.commit()
