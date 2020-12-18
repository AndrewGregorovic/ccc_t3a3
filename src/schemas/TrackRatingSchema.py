from marshmallow.validate import Range

from src.main import ma
from src.models.TrackRating import Track_Rating


class TrackRatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track_Rating

    rating = ma.Integer(required=True, validate=Range(min=1, max=5))
    user_id = ma.Integer()
    track = ma.Nested("TrackSchema", only=("id", "href", "name", "duration_ms", "explicit", "popularity", "uri"))


trackrating_schema = TrackRatingSchema()
trackratings_schema = TrackRatingSchema(many=True)
