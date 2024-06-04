import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
from models import app, db, Genres

cid = '743874e5946242aca7a2b78363605dd4'
secret = '4eb091f3739444ae9be89cf86154eb58'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

auth = SpotifyClientCredentials(client_id=cid,client_secret=secret)
token = auth.get_access_token()
spotify = spotipy.Spotify(auth=token)

def create_genre(sp):
    '''
    gets artists and tracks for 100 genres
    '''
    print('Creating genres...')
    # get list of genres 
    genres_list = sp.recommendation_genre_seeds()['genres'][:100]
    for genre in genres_list:
        # name
        name = genre

        # artists
        related_artists = sp.search(q='genre:' + genre, type='artist', limit=3)['artists']['items']
        artists = json.dumps([artist['name'] for artist in related_artists])
        artist_ids = json.dumps([artist['id'] for artist in related_artists])

        # average popularity
        if related_artists:
            popularity = sum([artist['popularity'] for artist in related_artists]) / len(related_artists)
        else:
            popularity = 0

        # albums
        related_albums = [sp.search(q='artist:' + artist['name'], type='album')['albums']['items'][0] for artist in related_artists]
        albums = json.dumps([album['name'] for album in related_albums])
        album_ids = json.dumps([album['id'] for album in related_albums])

        # tracks
        tracks = sp.search(q='genre:' + genre, type='track', limit=3)['tracks']['items']
        track_names = json.dumps([track['name'] for track in tracks])

        # create genre instance and add to db
        newGenre = Genres(name = name, artists = artists, artist_ids = artist_ids, albums = albums, album_ids = album_ids, tracks = track_names, popularity = popularity)
        db.session.add(newGenre)
        db.session.commit()

# db.drop_all()
# db.create_all()

# create_genre(sp)