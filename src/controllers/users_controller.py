from flask import abort, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.User import User
from src.schemas.UserSchema import user_schema


users = Blueprint("users", __name__)


@users.route("/me", methods=["GET"])
@jwt_required
def get_user():
    """
    Gets the current user's profile

    Returns:
    Dict of the retrieved user
    """

    user = User.query.get(get_jwt_identity())

    if not user:
        return abort(404, description="User not found.")

    return jsonify(user_schema.dump(user))
