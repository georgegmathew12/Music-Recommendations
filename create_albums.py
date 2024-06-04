import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from models import app, db, Albums, Artists
import json

cid = '743874e5946242aca7a2b78363605dd4'
secret = '4eb091f3739444ae9be89cf86154eb58'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


auth = SpotifyClientCredentials(client_id=cid,client_secret=secret)
token = auth.get_access_token()
spotify = spotipy.Spotify(auth=token)

"""
    GET INFORMATION FOR DB FOR THESE PARAMETERS:
        id
        name
        artist
        artist_id
        image
        info
        tracks
        genres
"""

#query list of artist ids from the database and store in variable
def query_artist_ids():
    artist_ids = Artists.query.with_entities(Artists.id).all()
    return [id[0] for id in artist_ids]


"""FOR DEBUGGING ONLY
#Test function with random artist id's generated
def get_artist_ids(sp, num_artists=50):
    unique_artist_ids = set()

    while len(unique_artist_ids) < num_artists:
        # Use the browse 'categories' endpoint to find playlists, then get artists from there
        categories = sp.categories(limit=50)['categories']['items']
        for category in categories:
            playlists = sp.category_playlists(category_id=category['id'], limit=50)['playlists']['items']
            for playlist in playlists:
                try:
                    tracks = sp.playlist_tracks(playlist['id'], limit=100)['items']
                    for track in tracks:
                        # Check if track and artists exist
                        if track['track'] and track['track']['artists']:
                            artist_id = track['track']['artists'][0]['id']
                            unique_artist_ids.add(artist_id)
                            if len(unique_artist_ids) >= num_artists:
                                return list(unique_artist_ids)
                except spotipy.SpotifyException as e:
                    print(f"Error processing playlist {playlist['id']}: {e}")

    return list(unique_artist_ids)
"""


#get and add first album released by artist for every artist in [artist_names]
def create_album(sp):
    print('Creating albums...')
    artist_ids = query_artist_ids()
    """For debugging only
    try:
        artist_ids = get_artist_ids(sp, num_artists=50) # Get unique artist IDs
    except Exception as e:
        print(f"An error occurred: {e}")
    """

    # call method to show every album released by that artist
    for artist_id in artist_ids:
        show_artist_albums(sp, artist_id)
            

"""
SHOWS ARTIST ALBUMS AND ADDS TO DB
#call spotify to fetch albums by artist's id (input param) - only albums should be fetched
#LIMIT set to 1 to just get 1 album for speed and simplicity
"""
def show_artist_albums(sp, artist_id):
    try:
        results = sp.artist_albums(artist_id, album_type='album', limit=1)
        if not results['items']:
            print(f"No albums found for artist with ID {artist_id}.")
            return None
        
        first_album = results['items'][0]
        album_details = sp.album(first_album['id'])

        track_names = [track['name'] for track in album_details['tracks']['items']]
        album_image = album_details['images'][0]['url'] if album_details['images'] else None
        album_info = {
            'release_date': album_details.get('release_date', 'Unknown release date'),
            'total_tracks': album_details.get('total_tracks', 0)
        }
        artist_info = sp.artist(artist_id)
        genres = artist_info.get('genres', [])

        # Check if the album is already in the database
        if not Albums.query.get(first_album['id']):
            newAlbum = Albums(
                id=first_album['id'],
                name=first_album['name'],
                artist=json.dumps([artist_info['name']]),
                artist_id=json.dumps([artist_id]),
                image=album_image,
                info=json.dumps(album_info),
                tracks=json.dumps(track_names),
                genres=json.dumps(genres)
            )
            db.session.add(newAlbum)
            db.session.commit()
        else:
            print(f"Album {first_album['id']} already exists in the database.")

    except spotipy.SpotifyException as e:
        print(f"Failed to fetch albums for artist ID {artist_id}: {e}")
        db.session.rollback()


# db.drop_all()
# db.create_all()

# create_album(sp)