from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os

from main.data_engineer.backend.sql_models.models import db

UPLOAD_FOLDER = "enrollment_database"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

from main.data_engineer.backend.api.routes import api_bp
app.register_blueprint(api_bp, url_prefix="/api")
