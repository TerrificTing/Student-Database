import sys
import os
from dotenv import load_dotenv
from flask import url_for, Flask

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.api.auth import google_bp 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")  #  Gets the Secret Key from the .env file
    app.register_blueprint(google_bp, url_prefix='/google')

    # Other app configurations and routes
    @app.route('/')
    def home():
        return '<h1>Home – Go to <a href="/google/login">Google Login</a></h1>'

    @app.route('/dashboard')
    def dashboard():
        return '<h1>Dashboard – You’re logged in!</h1>'
    
    @app.route('/check-redirect-uri')
    def check_redirect_uri():
        uri = url_for("google.authorized", _external=True)
        return f"Redirect URI is: <code>{uri}</code>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # Run the app in debug mode for development
