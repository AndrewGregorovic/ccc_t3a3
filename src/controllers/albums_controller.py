from flask import abort, Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_optional

from src.main import db
from src.models.Album import Album
from src.models.User import User
from src.models.Track import Track
from src.models.TrackRating import Track_Rating


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
        album.user_rating = round(db.session.query(db.func.avg(Track_Rating.rating))
                                  .join(Track)
                                  .filter(Track_Rating.user_id == user.id)
                                  .filter(Track.album_id == album_id)
                                  .scalar()
                                  )

        for track in album.tracks:
            track_rating = Track_Rating.query.filter_by(user_id=user.id, track_id=track.id).first()
            if track_rating:
                track.user_rating = track_rating.rating

    for track in album.tracks:
        track.duration_min = str(int(track.duration_ms / 1000 // 60))
        track.duration_sec = str(round(track.duration_ms / 1000 % 60))
        if int(track.duration_sec) < 10:
            track.duration_sec = f"0{track.duration_sec}"

    return render_template("album.html", album=album)
