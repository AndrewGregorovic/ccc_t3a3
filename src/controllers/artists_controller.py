from flask import abort, Blueprint, render_template

from src.models.Artist import Artist


artists = Blueprint("artists", __name__, url_prefix="/artists")


@artists.route("/", methods=["GET"])
def get_artists():
    """
    Gets all artists from the database

    Returns:
    List of dicts of artists
    """

    artists = Artist.query.all()

    return render_template("artists.html", artists=artists)


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

    return render_template("artist.html", artist=artist)
