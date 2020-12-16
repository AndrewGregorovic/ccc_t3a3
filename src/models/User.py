from src.main import db
from src.models.TrackRating import track_ratings


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(2), nullable=True)
    display_name = db.Column(db.String(30), nullable=True)
    href = db.Column(db.String(), nullable=False)
    product = db.Column(db.String(20), nullable=False, default="free")
    object_type = db.Column(db.String(20), nullable=False, default="user")
    uri = db.Column(db.String(), nullable=False)
    track_ratings = db.relationship(track_ratings)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.email}>"
