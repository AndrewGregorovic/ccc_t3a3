from src.main import db


class Track_Rating(db.Model):
    __tablename__ = "track_ratings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    track = db.relationship("Track")
