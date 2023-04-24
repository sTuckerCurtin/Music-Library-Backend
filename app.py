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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255))
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(255))
    
    def __repr__(self):
        return f"{self.title} {self.artist} {self.album} {self.release_date} {self.genre}"



# Schemas
class SongSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "artist", "album", "release_date", "genre")


song_schema = SongSchema()
songs_schema = SongSchema(many=True)



# Resources
class SongListResource(Resource):
    def get(self):
        all_songs = Song.query.all()
        return songs_schema.dump(all_songs)
    
    def post(self):
        print(request)
        new_song = Song(
            title=request.json["title"],
            artist=request.json["artist"],
            album=request.json["album"],
            release_date=request.json["release_date"],
            genre=request.json["genre"]
        )
        db.session.add(new_song)
        db.session.commit()
        return song_schema.dump(new_song), 201
        
class SongResource(Resource):
    def get(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)
        return song_schema.dump(song_from_db)
    
    def delete(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)
        db.session.delete(song_from_db)
        db.session.commit()
        return "", 204
    

    def put(self, song_id):
        song_from_db = Song.query.get_or_404(song_id)

        if "title" in request.json:
            song_from_db.title = request.json["title"]
        
# Routes
api.add_resource(SongListResource, "/api/songs")
api.add_resource(SongResource, "/api/songs/<int:song_id>")
