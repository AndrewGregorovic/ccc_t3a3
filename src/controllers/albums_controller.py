from flask import abort, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_optional

from src.main import db
from src.models.Album import Album
from src.models.User import User
from src.models.Track import Track
from src.models.TrackRating import Track_Rating
from src.schemas.AlbumSchema import album_schema


albums = Blueprint("albums", __name__, url_prefix="/albums")


@albums.route("/<int:album_id>", methods=["GET"])
@jwt_optional
def get_album(album_id):
    """
    Gets a single album

    If a JWT is provided it will use the users ratings for the tracks in the album
    to calculate the average rating for the album and include it in the output

    Parameters:
    album_id: integer
        The id number of the album

    Returns:
    Dict of the retrieved album
    """

    album = Album.query.get(album_id)

    if not album:
        return abort(404, description="Album not found.")

    id = get_jwt_identity()

    if id:
        user = User.query.get(id)
        album.album_rating = round(db.session.query(db.func.avg(Track_Rating.rating))
                                   .join(Track)
                                   .filter(Track_Rating.user_id == user.id)
                                   .filter(Track.album_id == album_id)
                                   .scalar()
                                   )

    return jsonify(album_schema.dump(album))
