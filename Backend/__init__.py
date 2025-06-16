from flask import Flask, render_template
from Backend.auth import google_bp  # Import the Google login blueprint
import os

def create_app():
    app = Flask(__name__, template_folder = '../Frontend/templates')
    app.secret_key = os.getenv("FLASK_SECRET_KEY")  # You can also load this from .env or config
    
    # Register Blueprints
    app.register_blueprint(google_bp, url_prefix='/google_login')

    @app.route('/')
    def index():
        return render_template('frontend.html')  # Returns an HTML page

    return app
