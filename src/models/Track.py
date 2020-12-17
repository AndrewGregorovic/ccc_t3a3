from src.main import db


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    album = db.relationship("Album", back_populates="tracks")
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artist", back_populates="tracks")
    disc_number = db.Column(db.Integer, nullable=True, default=1)
    duration_ms = db.Column(db.Integer, nullable=False)
    explicit = db.Column(db.Boolean, nullable=False, default=False)
    href = db.Column(db.String(), nullable=False, default="https://api.spotify.com/tracks/<id>")
    name = db.Column(db.String(), nullable=False)
    popularity = db.Column(db.Integer, nullable=False, default=0)
    preview_url = db.Column(db.String(), nullable=False, default="https://p.scdn.co/mp3-preview/<id>")
    track_number = db.Column(db.Integer, nullable=False)
    object_type = db.Column(db.String(20), nullable=False, default="track")
    uri = db.Column(db.String(), nullable=False, default="spotify:track:<id>")
    is_local = db.Column(db.Boolean, nullable=False, default=False)
