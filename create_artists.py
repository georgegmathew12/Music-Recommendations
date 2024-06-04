import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
from models import app, db, Artists

#* Set up spotipy variables, tokens, etc.
cid = '743874e5946242aca7a2b78363605dd4'
secret = '4eb091f3739444ae9be89cf86154eb58'
auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# auth = SpotifyClientCredentials(client_id=cid,client_secret=secret)
# token = auth.get_access_token()
# spotify = spotipy.Spotify(auth=token)

#TODO: artist_id (string) --> {artist_name (string), artist_image (array of object), artist_popularity (integer), artist_genres (array of strings), 
#TODO: -- other GET requests -- artist_tracks, artist_albums, related_artists}
#TODO: Need 100 
#* Steps:
#1. search for 100 random artists, save artist ID
#2. use artist ID's url, loop and collect: name, image, pop, genres 
#3. use artist tracks url, get tracks
#4. use artist albums url, get all albums
#5. use related artists url, get related artists
#6. get album ids by looping through retrieved album items and pulling ids
#7. store info in models.py db file
#! note, using spotipy library, dont have to use urls, can use spotipy functions

def create_artist(sp):
    print('Creating artists...')
    for offset in range(0, 50, 50): 
        artist_results = sp.search(q='year:2020', type='artist', limit=50, offset=offset)['artists']['items'] #spotify limits to 50 for a single search
        # print("Number of artists processed (Batch 1):", len(artist_results))
        # print("Sample artist data (Batch 1):", artist_results[0])
        
        album_ids = []  # Separate list for album IDs
        
        for artist in artist_results:
            id = artist['id']
            name = artist['name']
            image = json.dumps(artist['images'])
            popularity = artist['popularity']
            followers = artist['followers']['total']
            genres = json.dumps(artist['genres'])

            track_search = sp.search(q='artist:' + name, type='track', limit=5)['tracks']['items']
            tracks = json.dumps([track['name'] for track in track_search])

            album_search = sp.search(q='artist:' + name, type='album')['albums']['items']
            albums = json.dumps([album['name'] for album in album_search])
            album_ids = json.dumps([album['id'] for album in album_search])

            related_artists = json.dumps(sp.artist_related_artists(artist['id'])['artists'])
            
            new_artist = Artists(id=id, name=name, image=image, popularity=popularity, followers=followers, genres=genres,
                                 tracks=tracks, albums=albums, related_artists=related_artists, albums_id=album_ids)
            db.session.add(new_artist)
        
        db.session.commit()
        print("Batch 1 of artists added")

    for offset in range(50, 100, 50): #for second batch of artists to get 100; can keep repeating for x artists
        artist_results = sp.search(q='year:2020', type='artist', limit=50, offset=offset)['artists']['items']
        # print("Number of artists processed (Batch 2):", len(artist_results))
        # print("Sample artist data (Batch 2):", artist_results[0])
        
        album_ids = []  # Separate list for album IDs
        
        for artist in artist_results:
            id = artist['id']
            name = artist['name']
            image = json.dumps(artist['images'])
            popularity = artist['popularity']
            genres = json.dumps(artist['genres'])

            track_search = sp.search(q='artist:' + name, type='track', limit=10)['tracks']['items']
            tracks = json.dumps([track['name'] for track in track_search])

            album_search = sp.search(q='artist:' + name, type='album')['albums']['items']
            albums = json.dumps([album['name'] for album in album_search])
            album_ids = json.dumps([album['id'] for album in album_search])

            related_artists = json.dumps(sp.artist_related_artists(artist['id'])['artists'][:5])
            
            new_artist = Artists(id=id, name=name, image=image, popularity=popularity, genres=genres,
                                 tracks=tracks, albums=albums, related_artists=related_artists, albums_id=album_ids)
            db.session.add(new_artist)
        
        db.session.commit()
        print("Batch 2 of artists added")

# db.drop_all()
# db.create_all()

# create_artist(sp)