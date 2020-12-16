import random

from faker import Faker
from flask import Blueprint

from src.main import bcrypt, db
from src.models.Album import Album
from src.models.Artist import Artist
from src.models.Track import Track
from src.models.TrackRating import Track_Rating
from src.models.User import User


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    """
    Custom flask db command to create all tables from models
    """

    db.create_all()
    print("TABLES CREATED")


@db_commands.cli.command("drop")
def drop_db():
    """
    Custom flask db command to drop all tables from the database
    """

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("TABLES DROPPED")


@db_commands.cli.command("seed")
def seed_db():
    """
    Custom flask db command to seed tables with fake data for testing
    """

    faker = Faker()

    users = []
    for i in range(10):
        user = User()
        user.display_name = f"testuser{i + 1}"
        user.email = f"test{i + 1}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)

    admin = User()
    admin.display_name = "admin"
    admin.email = "admin@test.com"
    admin.password = bcrypt.generate_password_hash("admin").decode("utf-8")
    admin.admin = True
    db.session.add(admin)

    db.session.commit()

    genres = ["rock", "pop", "instrumental", "jazz", "metal", "hip-hop", "country"]
    labels = ["Warner Music Group", "EMI", "Sony Music", "BMG", "Universal Music Group", "PolyGram"]
    copyright_types = ["C", "P"]

    artists = []
    for i in range(5):
        artist = Artist()
        artist.name = f"artist {i + 1}"
        artist.followers = random.randint(1, 10000)
        artist.genre = random.choice(genres)
        artist.popularity = random.randint(1, 100)
        db.session.add(artist)
        artists.append(artist)

    db.session.commit()

    albums = []
    for i in range(10):
        album = Album()
        album.name = f"album {i + 1}"
        album.copyright = faker.catch_phrase()
        if len(album.copyright) > 100:
            album.copyright = album.copyright[:99]
        album.copyright_type = random.choice(copyright_types)
        album.label = random.choice(labels)
        album.release_date = random.randint(1990, 2020)
        artist = random.choice(artists)
        album.artist_id = artist.id
        album.genre = artist.genre
        artist.albums.append(album)
        albums.append(album)

    db.session.commit()

    tracks = []
    for album in albums:
        number_of_tracks = random.randint(1, 12)
        for i in range(number_of_tracks):
            track = Track()
            track.name = faker.catch_phrase()
            track.duration_ms = random.randint(180000, 300000)
            track.explicit = random.choice([True, False])
            track.popularity = random.randint(1, 100)
            track.track_number = i + 1
            track.is_local = random.choice([True, False])
            track.album_id = album.id
            artist = album.artist
            track.artist_id = artist.id
            album.tracks.append(track)
            artist.tracks.append(track)
            tracks.append(track)

    db.session.commit()

    for track in tracks:
        for user in users:
            trackrating = Track_Rating()
            trackrating.track_id = track.id
            trackrating.user_id = user.id
            trackrating.rating = random.randint(0, 5)
            user.track_ratings.append(trackrating)

    db.session.commit()

    print("TABLES SEEDED")
