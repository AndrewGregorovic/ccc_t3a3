from flask import abort, Blueprint, jsonify

from src.models.Album import Album
from src.schemas.AlbumSchema import album_schema


albums = Blueprint("albums", __name__, url_prefix="/albums")


@albums.route("/<int:album_id>", methods=["GET"])
def get_album(album_id):
    """
    Gets a single album

    Parameters:
    album_id: integer
        The id number of the album

    Returns:
    Dict of the retrieved album
    """

    album = Album.query.get(album_id)

    if not album:
        return abort(404, description="Album not found.")

    return jsonify(album_schema.dump(album))
