from marshmallow.validate import Equal, Length, OneOf, Range

from src.main import ma
from src.models.Album import Album


class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album
        dump_only = ["user_rating"]

    album_type = ma.String(validate=[
        Length(max=20),
        OneOf(["album", "compilation", "single"])
    ])
    artist = ma.Nested("ArtistSchema", only=("id", "href", "name", "object_type", "uri"))
    copyright = ma.String(required=True, validate=Length(max=100))
    copyright_type = ma.String(required=True, validate=[
        Length(max=1),
        OneOf(["C", "P"])
    ])
    genre = ma.String(required=True, validate=Length(max=20))
    href = ma.String()
    label = ma.String(required=True, validate=Length(max=50))
    name = ma.String(required=True)
    release_date = ma.Integer(required=True, validate=Range(min=1, max=2020))
    release_date_precision = ma.String(required=True, validate=Equal("year"))
    object_type = ma.String(required=True, validate=Equal("album"))
    tracks = ma.Nested("TrackSchema", many=True, only=("id", "href", "name", "duration_ms", "duration_min", "duration_sec", "explicit", "popularity", "uri", "user_rating"))
    uri = ma.String()
    user_rating = ma.Integer(validate=Range(min=1, max=5))


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)
