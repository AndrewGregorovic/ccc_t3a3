# import gzip

# from sh import pg_dump
from flask import jsonify
from sqlalchemy import text

from src.main import db
from src.schemas.AlbumSchema import albums_schema
from src.schemas.ArtistSchema import artists_schema
from src.schemas.TrackRatingSchema import trackratings_schema
from src.schemas.TrackSchema import tracks_schema
from src.schemas.UserSchema import users_schema


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    # def dump_database():
    #     """
    #     Method to dump the database contents to a file using pg_dump

    #     Returns:
    #     String with message on whether or not the dump was successful
    #     """

    #     try:
    #         with gzip.open("database_dump.gz", "wb") as f:
    #             pg_dump("-h", "localhost", "-U", "t3a3", "t3a3", _out=f)
    #     except Exception:
    #         return "An error occurred and the database was unable to be dumped"

    #     return "Database dumped to file 'database_dump.gz'"

    def dump_database():
        """
        Method to dump the database as json using SQL commands

        Returns:
        Json of the contents of each table in the database
        """

        albums = albums_schema.dump(db.engine.execute(text("SELECT * FROM albums;")))
        artists = artists_schema.dump(db.engine.execute(text("SELECT * FROM artists;")))
        tracks = tracks_schema.dump(db.engine.execute(text("SELECT * FROM tracks;")))
        trackratings = trackratings_schema.dump(db.engine.execute(text("SELECT * FROM track_ratings;")))
        users = users_schema.dump(db.engine.execute(text("SELECT * FROM users;")))

        return jsonify(albums, artists, tracks, trackratings, users)
