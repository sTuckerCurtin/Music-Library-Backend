from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Song(db.Model):
    id = db.column(db.Integer, priary_key=True)
    title = db.column (db.String(255), nullable=False)
    artist = db.column (db.String(255), nullable=False)
    album = db.column (db.String(255))
    release_date = db.column (db.String(255))
    genre = db.column(db.String(255))
    
    def __repr__(self):
        return f"{self.title} {self.artist} {self.album} {self.release_date} {self.genre}"


# Schemas



# Resources



# Routes
