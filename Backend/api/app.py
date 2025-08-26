from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from Backend.api.auth import google_bp, create_user_database
from Backend.api.models import User

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with env var for production

# Register blueprint
app.register_blueprint(google_bp, url_prefix="/login")

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "google.login"

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def home():
    return '''
        <h1>Welcome!</h1>
        <p>Click here to <a href="/login/auth">Login with Google</a>.</p>
    '''
# Example protected route
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.username}!"

# Initialize DB
with app.app_context():
    create_user_database()

# No `if __name__ == "__main__"` needed for Vercel
