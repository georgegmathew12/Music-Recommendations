from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import app, db, Artists, Albums, Genres

@app.route('/artists/JSON')
def bookJSON():
    r = json.dumps(artists)
    return r


# Showing the About Page
@app.route('/about')
def about():
    return render_template('about.html')

# ------------
# artistjson
# ------------	
@app.route('/artist/json/')
def artistjson():
    """
    turn your /artist/json/ of objects into a list of serializable values
    """
    artists = db.session.query(Artists).all()
    return jsonify(Artists=[e.serialize() for e in artists])


# ------------
# albumjson
# ------------	
@app.route('/album/json/')
def albumjson():
    """
    turn your /album/json/ of objects into a list of serializable values
    """
    albums = db.session.query(Albums).all()
    return jsonify(Albums=[e.serialize() for e in albums])


# ------------
# genrejson
# ------------	
@app.route('/genre/json/')
def genrejson():
    """
    turn your /genre/json/ of objects into a list of serializable values
    """
    genres = db.session.query(Genres).all()
    return jsonify(Genres=[e.serialize() for e in genres])



@app.route('/')
# Showing A List Artist In Database
@app.route('/artists/')
def showArtists():
	artists_list = db.session.query(Artists).all()
	return render_template('showAllArtists.html', artists_list = artists_list)


# Showing A List Albums In Database
@app.route('/albums/')
def showAlbums():
    if albums:
        albums_list = db.session.query(musicdb).all()
        return render_template('showAllAlbums.html', albums_list = albums_list)
    else:
        return "Albums not found", 404
    
# Showing A List Genres In Database
@app.route('/genres/')
def showGenres():
    if genres:
        genres_list = db.session.query(Genres).all()
        return render_template('showAllAlbums.html', genres_list = genres_list)
    else:
        return "Genres not found", 404

# Showing all Artists related on another Artists
@app.route('/<artist_name>/relatedArtists')
def relatedArtists(artist_name):
    artist = None
    for a in artists:
        if a['name'] == artist_name:
            artist = a
            break
    if artist:
        return render_template('relatedArtists.html', artist = artist, relatedArtists = relatedArtists)
    else:
        return "Artist not found", 404
    
# Showing A Single Genre In Database
@app.route('/genre/<genre_name>/',  methods=['GET', 'POST'])
def showGenre(genre_name):
    genre = db.session.query(Genres).filter(Genres.name == genre_name).first()
    return jsonify(genre.serialize()) if genre else ("Record not found", 400)
    # genre = None
    # for g in genres:
    #     if g['name'] == genre_name:
    #         genre = g
    #         break
    # if genre:
    #     return render_template('showGenre.html', genre = genre)
    # else:
    #     return "Genre not found", 404
    
# Showing A Single Album In Database
@app.route('/album/<album_name>/',  methods=['GET', 'POST'])
def showAlbum(album_name):
    album = db.session.query(Albums).filter(Albums.name == album_name).first()
    return jsonify(album.serialize()) if album else ("Record not found", 400)

# Showing A Single Artist In Database
@app.route('/artist/<artist_name>/')
def showArtist(artist_name):
    artist = db.session.query(Artists).filter(Artists.name == artist_name).first()
    return jsonify(artist.serialize()) if artist else ("Record not found", 400)

if __name__ == "__main__":
    app.debug = True
    app.run()
