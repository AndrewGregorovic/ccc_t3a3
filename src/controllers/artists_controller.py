from flask import abort, Blueprint, jsonify

from src.models.Artist import Artist
from src.schemas.ArtistSchema import artist_schema, artists_schema


artists = Blueprint("artists", __name__, url_prefix="/artists")


@artists.route("/", methods=["GET"])
def get_artists():
    """
    Gets all artists from the database

    Returns:
    List of dicts of artists
    """

    artists = Artist.query.all()

    return jsonify(artists_schema.dump(artists))


@artists.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """
    Gets a single artist

    Parameters:
    artist_id: integer
        The id number of the artist

    Returns:
    Dict of the retrieved artist
    """

    artist = Artist.query.get(artist_id)

    if not artist:
        return abort(404, description="Artist not found.")

    return jsonify(artist_schema.dump(artist))
