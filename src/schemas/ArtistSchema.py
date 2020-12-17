from marshmallow.validate import Equal, Length, Range

from src.main import ma
from src.models.Artist import Artist


class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist

    albums = ma.Nested("AlbumSchema", many=True, only=("album_type", "id", "href", "name", "release_date", "uri"))
    followers = ma.Integer()
    genre = ma.String(required=True, validate=Length(max=20))
    href = ma.String()
    name = ma.String(required=True)
    popularity = ma.Integer(validate=Range([1, 100]))
    object_type = ma.String(required=True, validate=Equal("artist"))
    tracks = ma.Nested("TrackSchema", many=True, only=("id", "href", "name", "duration_ms", "explicit", "popularity", "uri"))
    uri = ma.String()


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
