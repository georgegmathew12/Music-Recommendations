# import modules and libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# initializing Flask app 
app = Flask(__name__)

# Database Info
app.app_context().push()
# Change this accordingly 
USER ="postgres"
PASSWORD = "Iamthesqlmaster92?!"
PUBLIC_IP_ADDRESS ="localhost:5432"
DBNAME ="musicdb"

# Configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_STRING", f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)



# Artists
# ------------
class Artists(db.Model):
    """
    Artists class attrbiutes 

    id
    name
    image
    info
    tracks
    albums
    genres
    related_artists

    """
    __tablename__ = 'artists'

    id = db.Column(db.String(1024), primary_key = True)
    name = db.Column(db.String(1024), nullable = False)
    image = db.Column(db.Text, nullable = False)
    popularity = db.Column(db.Integer, nullable = False)
    followers = db.Column(db.Integer)
    tracks = db.Column(db.Text, nullable = False)
    albums = db.Column(db.Text, nullable = False)
    genres = db.Column(db.Text, nullable = False)
    related_artists = db.Column(db.Text, nullable = False)
    albums_id = db.Column(db.Text, nullable = False) 

    # ------------
    # serialize
    # ------------
    def serialize(self):
       """
       returns a dictionary
       """
       return {
          'id': self.id, 
          'name': self.name,
          'image': self.image, 
          'popularity': self.popularity, 
          'followers': self.followers,
          'tracks': self.tracks, 
          'albums': self.albums,  
          'genres': self.genres, 
          'related_artists': self.related_artists,    
          'albums_id': self.albums_id
        }


# ------------
# Albums
# ------------
class Albums(db.Model):
    """
    Albums class attrbiutes 

    id
    name
    artist
    artist_id
    image
    info
    tracks
    genres

    """
    __tablename__ = 'albums'

    id = db.Column(db.String(512), primary_key = True)
    name = db.Column(db.String(512),  nullable = False)
    artist = db.Column(db.String(512), nullable = False)
    artist_id = db.Column(db.String(512), nullable = False)
    image = db.Column(db.String(512), nullable = False)
    info = db.Column(db.JSON, nullable=False)
    tracks = db.Column(db.Text, nullable=False)
    genres = db.Column(db.String(512), nullable = False)

    # ------------
    # serialize
    # ------------
    def serialize(self):
       """
       returns a dictionary
       """
       return {
          'id': self.id, 
          'name': self.name,
          'artist': self.artist,
          'artist_id': self.artist_id, 
          'image': self.image,
          'info': self.info,  
          'tracks': self.tracks, 
          'genres': self.genres    
        }


# ------------
# Genres
# ------------
    
class Genres(db.Model):
    """
    Genres class attrbiutes 

    name
    artist
    artist_id
    albums
    albums_id
    tracks
    popularity
    """

    __tablename__ = 'genres'

    name = db.Column(db.String(512), primary_key = True)
    artists = db.Column(db.Text, nullable = False)
    artist_ids = db.Column(db.Text, nullable = False)
    albums = db.Column(db.Text, nullable = False)
    album_ids = db.Column(db.Text, nullable = False)
    tracks = db.Column(db.Text, nullable = False)
    popularity = db.Column(db.Integer, nullable = False)
    
    # ------------
    # serialize
    # ------------
    def serialize(self):
       """
       returns a dictionary
       """
       return {
          'name': self.name,
          'artists': self.artists,
          'artist_ids': self.artist_ids,
          'albums': self.albums,
          'album_ids': self.album_ids,
          'tracks': self.tracks,
          'popularity': self.popularity
        } 


with app.app_context():
   db.drop_all()
   db.create_all()