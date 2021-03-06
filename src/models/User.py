from src.main import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(2), nullable=True)
    display_name = db.Column(db.String(30), nullable=True)
    href = db.Column(db.String(), nullable=False, default="https://api.spotify.com/users/<id>")
    product = db.Column(db.String(20), nullable=False, default="free")
    object_type = db.Column(db.String(20), nullable=False, default="user")
    uri = db.Column(db.String(), nullable=False, default="spotify:user:<id>")
    track_ratings = db.relationship("Track_Rating", backref="user")
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.email}>"
