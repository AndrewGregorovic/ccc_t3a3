from flask import abort, Blueprint, jsonify, request

from src.main import db
from src.models.Album import Album
from src.models.Artist import Artist
from src.models.Track import Track
from src.models.TrackRating import Track_Rating
from src.models.User import User
from src.schemas.TrackSchema import track_schema, tracks_schema


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


@tracks.route("/<int:track_id>/ratings", methods=["GET"])
def get_track_ratings(track_id):
    """
    Gets all the user ratings for a track

    Parameters:
    track_id: integer
        The id number of the track

    Returns:
    List of dicts containing data from both the users and track_ratings tables
    """

    track_ratings = db.session.query(User, Track_Rating)\
        .outerjoin(Track_Rating, User.id == Track_Rating.user_id)\
        .filter(Track_Rating.track_id == track_id)\
        .all()

    ratings_list = []
    for rating in track_ratings:
        if rating[1]:
            ratings_list.append({
                "user_display_name": rating[0].display_name,
                "user_href": rating[0].href,
                "user_id": rating[0].id,
                "user_uri": rating[0].uri,
                "rating": rating[1].rating,
                "track_id": rating[1].track_id
            })

    return jsonify(ratings_list)


@tracks.route("/", methods=["GET"])
def get_all_tracks():
    """
    Gets all tracks and orders them based on artist or album name depending on query string
    If no query string, tracks are ordered by track name

    Returns:
    List of dicts of tracks
    """

    if request.args and "orderby" in request.args:
        if request.args["orderby"] == "album":
            tracks = db.session.query(Track, Album)\
                .join(Album, Track.album_id == Album.id)\
                .order_by(Album.name, Track.name)\
                .all()
            tracks = [track[0] for track in tracks]
        elif request.args["orderby"] == "artist":
            tracks = db.session.query(Track, Artist)\
                .join(Artist, Track.artist_id == Artist.id)\
                .order_by(Artist.name, Track.name)\
                .all()
            tracks = [track[0] for track in tracks]
        else:
            tracks = Track.query.order_by(Track.name).all()
    else:
        tracks = Track.query.order_by(Track.name).all()

    return jsonify(tracks_schema.dump(tracks))
