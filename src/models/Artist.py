from src.main import db


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    albums = db.relationship("Album", back_populates="artist")
    followers = db.Column(db.Integer, nullable=False, default=0)
    genre = db.Column(db.String(20), nullable=False)
    href = db.Column(db.String(), nullable=False, default="http://spotify.com/artist/<id>")
    name = db.Column(db.String(), nullable=False)
    popularity = db.Column(db.Integer, nullable=False, default=0)
    object_type = db.Column(db.String(20), nullable=False, default="artist")
    tracks = db.relationship("Track", back_populates="artist")
    uri = db.Column(db.String(), nullable=False, default="spotify:artist:<id>")
