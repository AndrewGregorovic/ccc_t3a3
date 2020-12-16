from src.main import db


class Track_Rating(db.Model):
    __tablename__ = "track_ratings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=0)
    track = db.relationship("Track")

# track_ratings = db.Table("track_ratings", db.Model.metadata,
#                          db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
#                          db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True),
#                          db.Column("rating", db.Integer, nullable=False, default=0)
#                          db.relationship("Track")
#                          )
