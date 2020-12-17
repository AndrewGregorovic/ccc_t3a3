from marshmallow.validate import Equal, Range

from src.main import ma
from src.models.Track import Track


class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track

    album = ma.Nested("AlbumSchema", only=("album_type", "id", "href", "name", "release_date", "uri"))
    artist = ma.Nested("ArtistSchema", only=("id", "href", "name", "object_type", "uri"))
    disc_number = ma.Integer()
    duration_ms = ma.Integer(required=True)
    explicit = ma.Boolean()
    href = ma.String()
    name = ma.String(required=True)
    popularity = ma.Integer(validate=Range([1, 100]))
    preview_url = ma.String()
    track_number = ma.Integer(required=True)
    object_type = ma.String(required=True, validate=Equal("track"))
    uri = ma.String()
    is_local = ma.Boolean()


track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)
