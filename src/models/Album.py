from src.main import db


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    album_type = db.Column(db.String(20), nullable=False, default="album")
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artist", back_populates="albums")
    copyright = db.Column(db.String(100), nullable=False)
    copyright_type = db.Column(db.String(1), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    href = db.Column(db.String(), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Integer, nullable=False)
    release_date_precision = db.Column(db.String(5), nullable=False, default="year")
    object_type = db.Column(db.String(20), nullable=False, default="album")
    tracks = db.relationship("Track", back_populates="album")
    uri = db.Column(db.String(), nullable=False)
