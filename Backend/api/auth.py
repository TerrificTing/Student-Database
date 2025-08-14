from flask import Blueprint, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user
import os
from dotenv import load_dotenv
from Backend.api.models import User, get_db
from requests.exceptions import HTTPError

# Load environment variables from .env file
load_dotenv()

# Set up Google OAuth blueprint using environment variables
google_bp = make_google_blueprint(
    client_id = os.getenv("GOOGLE_CLIENT_ID"),  # Load from .env
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),  # Load from .env
    scope=["profile", "email"],
    redirect_to = "google_login"
)

def create_user_database():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
                CREATE TALBE IF NOT EXISTS users(
                google_id TEXT PRIMARY KEY,
                username TEXT NOT NULL)
                """)
    con.commit()

# Define Google login route
@google_bp.route("/login")
def google_login():
    try:
        if not google.authorized:
            return redirect(url_for("google.login"))

        try:
            # Get user info from Google
            google_info = google.get("/oauth2/v2/userinfo")
            google_info.raise_for_status()
        except HTTPError as e:
            print('Token expired or API error', e)
        user_info = google_info.json()
        google_id = user_info.get("id")
        username = user_info.get("name")

        # Debug print for development
        print("Google user info:", user_info)

        # Check if the user already exists in the database
        con = get_db()
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
        user = cur.fetchone()

        if not user:
            # If the user doesn't exist, create a new one
            cur.execute('INSERT INTO users (google_id, username) VALUES (?, ?)', (google_id, username))
            con.commit()

        # Create a User instance and log the user in
        user = User(id=google_id, username=username)
        login_user(user)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Interal Server Error: {e}", 500

    return redirect(url_for("dashboard"))
