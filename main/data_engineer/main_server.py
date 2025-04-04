from flask import Flask
from flask_cors import CORS
from sql.models import db
import os

UPLOAD_FOLDER = "enrollment_database"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask app setup
server = Flask(__name__)

CORS(server)

server.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB
db.init_app(server)
with server.app_context():
    db.create_all()

# Register API Blueprint
from api.routes import api_bp
server.register_blueprint(api_bp, url_prefix="/api")
