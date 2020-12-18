from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.main import db
from src.models.User import User
from src.models.Track import Track
from src.models.TrackRating import Track_Rating
from src.schemas.TrackRatingSchema import trackrating_schema


trackratings = Blueprint("trackratings", __name__, url_prefix="/me/trackratings")


@trackratings.route("/<int:track_id>", methods=["GET"])
@jwt_required
def get_trackrating(track_id):
    """
    Gets the user's rating for a single track

    Parameters:
    track_id: integer
        The id number of the track

    Returns:
    Dict of the retrieved track rating
    """

    user = User.query.get(get_jwt_identity())

    if not user:
        return abort(401, description="Invalid user.")

    trackrating = Track_Rating.query.get({"user_id": user.id, "track_id": track_id})

    if not trackrating:
        return abort(404, description="User does not have a rating for this track.")

    return jsonify(trackrating_schema.dump(trackrating))


@trackratings.route("/<int:track_id>", methods=["POST"])
@jwt_required
def add_trackrating(track_id):

    user = User.query.get(get_jwt_identity())

    if not user:
        return abort(401, description="Invalid user.")

    trackrating = Track_Rating.query.get({"user_id": user.id, "track_id": track_id})

    if trackrating:
        return abort(400, "User already has a rating for this track.")

    track = Track.query.get(track_id)

    if not track:
        return abort(404, description="No track found with the provided id.")

    trackrating_fields = trackrating_schema.load(request.json)

    new_trackrating = Track_Rating()
    new_trackrating.user_id = user.id
    new_trackrating.track_id = track_id
    new_trackrating.rating = trackrating_fields["rating"]
    new_trackrating.track = track

    db.session.add(new_trackrating)
    db.session.commit()

    return (jsonify(trackrating_schema.dump(new_trackrating)), 201)


@trackratings.route("/<int:track_id>", methods=["PUT"])
@jwt_required
def update_trackrating(track_id):

    user = User.query.get(get_jwt_identity())

    if not user:
        return abort(401, description="Invalid user.")

    trackratings = Track_Rating.query.filter_by(user_id=user.id, track_id=track_id)

    if trackratings.count() != 1:
        return abort(404, description="User does not have a rating for this track.")

    trackrating_fields = trackrating_schema.load(request.json)

    trackratings.update(trackrating_fields)
    db.session.commit()

    return jsonify(trackrating_schema.dump(trackratings[0]))
