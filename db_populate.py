import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
from models import app, db, Artists, Albums, Genres
from create_artists import create_artist
from create_albums import create_album, query_artist_ids, show_artist_albums
from create_genre import create_genre

# Set up spotipy variables
cid = 'd5b7dba93f4c473682a8c66000573200'
secret = '8324c98c7a5f4037b1384f1042bf3c1d'
auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

db.drop_all()
db.create_all()

create_artist(sp)
create_album(sp)
create_genre(sp)