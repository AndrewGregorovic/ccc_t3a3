from flask import abort, Blueprint, jsonify

from src.models.Track import Track
from src.schemas.TrackSchema import track_schema


tracks = Blueprint("tracks", __name__, url_prefix="/tracks")


@tracks.route("/<int:track_id>", methods=["GET"])
def get_track(track_id):
    """
    Gets a single track

    Parameters:
    track_id: integer
        The id number of the track

    Returns:
    Dict of the retrieved track
    """

    track = Track.query.get(track_id)

    if not track:
        return abort(404, description="Track not found.")

    return jsonify(track_schema.dump(track))
