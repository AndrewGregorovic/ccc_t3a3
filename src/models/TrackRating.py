from src.main import db


class Track_Rating(db.Model):
    __tablename__ = "track_ratings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    track = db.relationship("Track")

    def __repr__(self):
        return f"<Track_Rating User: {self.user_id}, Track: {self.track_id}>"
