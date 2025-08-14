from flask import Blueprint, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user
import os
from dotenv import load_dotenv
from Backend.api.models import User, get_db

# Load environment variables from .env file
load_dotenv()

# Set up Google OAuth blueprint using environment variables
google_bp = make_google_blueprint(
    client_id = os.getenv("GOOGLE_CLIENT_ID"),  # Load from .env
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),  # Load from .env
    scope=["profile", "email"],
    redirect_to = "google_login"
)

# Define Google login route
@google_bp.route("/login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    # Get user info from Google
    google_info = google.get("/v1/people/me")
    print('Google response OK?', google_info.ok)
    print('Google response text?', google_info.text)    
    assert google_info.ok, google_info.text
    user_info = google_info.json()

    google_info = google.get("/oauth2/v2/userinfo")
    username = user_info["displayName"]

    # Check if the user already exists in the database
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE google_id = ?', (google_info,))
    user = cur.fetchone()

    if not user:
        # If the user doesn't exist, create a new one
        cur.execute('INSERT INTO users (google_id, username) VALUES (?, ?)', (google_info, username))
        con.commit()

    # Create a User instance and log the user in
    user = User(id=google_info, username=username)
    login_user(user)

    return redirect(url_for("dashboard"))
