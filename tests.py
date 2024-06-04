import unittest
from models import db, Albums, Artists, Genres

# -----------
# DBTestCases
# -----------


class DBTestCases(unittest.TestCase):
    '''
    3 functions to test db:
        - insert new instance
        - update existing instance
        - delete instance

    3 models to test:
        - artists
        - albums
        - genres
    '''

    # TESTING ARTISTS
    def test_insert_artist(self):
        # create test artist to insert
        artist_id = "artist1"
        artist = Artists(
            id=artist_id,
            name="Test Artist",
            image="image_url",
            popularity=80,
            tracks="tracks_info",
            albums="albums_info",
            genres="genres_info",
            related_artists="related_artists_info",
            albums_id="album1"
        )
        # insert test artist
        db.session.add(artist)
        db.session.commit()

        # check if test artist is in db
        queried_artist = Artists.query.filter_by(id=artist_id).first()
        self.assertIsNotNone(queried_artist)
        self.assertEqual(queried_artist.id, artist_id)

        # delete test artist to clean up
        db.session.delete(queried_artist)
        db.session.commit()


    def test_update_artist(self):
        # create test artist to insert and update
        artist_id = "artist1"
        artist = Artists(
            id=artist_id,
            name="Test Artist",
            image="image_url",
            popularity=80,
            tracks="tracks_info",
            albums="albums_info",
            genres="genres_info",
            related_artists="related_artists_info",
            albums_id="album1"
        )
        # insert test artist
        db.session.add(artist)
        db.session.commit()

        # update test artist
        queried_artist = Artists.query.filter_by(id=artist_id).first()
        artist.name = "Artist After Update"
        db.session.commit()

        # check if test artist is updated
        updated_artist = Artists.query.filter_by(id=artist_id).first()
        self.assertEqual(updated_artist.name, "Artist After Update")

        # delete test artist to clean up
        db.session.delete(updated_artist)
        db.session.commit()
    

    def test_delete_artist(self):
        # create test artist to insert
        artist_id = "artist1"
        artist = Artists(
            id=artist_id,
            name="Test Artist",
            image="image_url",
            popularity=80,
            tracks="tracks_info",
            albums="albums_info",
            genres="genres_info",
            related_artists="related_artists_info",
            albums_id="album1"
        )
        # insert test artist
        db.session.add(artist)
        db.session.commit()

        # delete test artist
        db.session.delete(artist)
        db.session.commit()

        # check if test artist is deleted
        queried_artist = Artists.query.filter_by(id=artist_id).first()
        self.assertIsNone(queried_artist)


    # TESTING ALBUMS
    def test_insert_album(self):
        # create test album to insert
        album_id = "album1"
        album = Albums(
            id=album_id,
            name="Test Album",
            artist="Test Artist",
            artist_id="artist1",
            image="image_url",
            info={"year": 2020, "label": "Test Label"},
            tracks="tracks_info",
            genres="genre1"
        )
        # insert test album
        db.session.add(album)
        db.session.commit()

        # check if test album is in db
        queried_album = Albums.query.filter_by(id=album_id).first()
        self.assertIsNotNone(queried_album)
        self.assertEqual(queried_album.id, album_id)

        # delete test album to clean up
        db.session.delete(queried_album)
        db.session.commit()
    

    def test_update_album(self):
        # create test album to insert and update
        album_id = "album1"
        album = Albums(
            id=album_id,
            name="Test Album",
            artist="Test Artist",
            artist_id="artist1",
            image="image_url",
            info={"year": 2020, "label": "Test Label"},
            tracks="tracks_info",
            genres="genre1"
        )
        # insert test album
        db.session.add(album)
        db.session.commit()

        # update test album
        queried_album = Albums.query.filter_by(id=album_id).first()
        queried_album.name = "Album After Update"
        db.session.commit()

        # check if test album is updated
        updated_album = Albums.query.filter_by(id=album_id).first()
        self.assertEqual(updated_album.name, "Album After Update")

        # delete test album to clean up
        db.session.delete(updated_album)
        db.session.commit()
    

    def test_delete_album(self):
        # create test album to insert
        album_id = "album1"
        album = Albums(
            id=album_id,
            name="Test Album",
            artist="Test Artist",
            artist_id="artist1",
            image="image_url",
            info={"year": 2020, "label": "Test Label"},
            tracks="tracks_info",
            genres="genre1"
        )
        # insert test album
        db.session.add(album)
        db.session.commit()
        
        # delete test album
        db.session.delete(album)
        db.session.commit()

        # check if test album is deleted
        queried_album = Albums.query.filter_by(id=album_id).first()
        self.assertIsNone(queried_album)


    def test_insert_genre(self):
        # create test genre to insert
        genre_name = "genre1"
        genre = Genres(
            name=genre_name,
            artists="Test Artist",
            artist_ids="artist1",
            albums="Test Album",
            album_ids="album1",
            tracks="tracks_info",
            popularity=80
        )
        # insert test genre
        db.session.add(genre)
        db.session.commit()

        # check if test genre is in db
        queried_genre = Genres.query.filter_by(name=genre_name).first()
        self.assertIsNotNone(queried_genre)
        self.assertEqual(queried_genre.name, genre_name)

        # delete test genre to clean up
        db.session.delete(queried_genre)
        db.session.commit()

    def test_update_genre(self):
        # create test genre to insert and update
        genre_name = "genre1"
        genre = Genres(
            name=genre_name,
            artists="Test Artist",
            artist_ids="artist1",
            albums="Test Album",
            album_ids="album1",
            tracks="tracks_info",
            popularity=80
        )
        # insert test genre
        db.session.add(genre)
        db.session.commit()

        # update test genre
        queried_genre = Genres.query.filter_by(name=genre_name).first()
        self.assertIsNotNone(queried_genre)
        self.assertEqual(queried_genre.name, genre_name)

        # update test genre
        queried_genre.name = "Genre After Update"
        db.session.commit()
        
        # check if test genre is updated
        updated_genre = Genres.query.filter_by(name=queried_genre.name).first()
        self.assertEqual(updated_genre.name, "Genre After Update")

        # delete test genre to clean up
        db.session.delete(updated_genre)
        db.session.commit()
    

    def test_delete_genre(self):
        # create test genre to insert
        genre_name = "genre1"
        genre = Genres(
            name=genre_name,
            artists="Test Artist",
            artist_ids="artist1",
            albums="Test Album",
            album_ids="album1",
            tracks="tracks_info",
            popularity=80
        )
        # insert test genre
        db.session.add(genre)
        db.session.commit()

        # delete test genre
        db.session.delete(genre)
        db.session.commit()

        # check if test genre is deleted
        queried_genre = Genres.query.filter_by(name=genre_name).first()
        self.assertIsNone(queried_genre)

if __name__ == '__main__':
    unittest.main()