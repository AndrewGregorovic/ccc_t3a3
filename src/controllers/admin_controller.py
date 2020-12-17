from flask import abort, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.Admin import Admin
from src.models.User import User


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/dumpdatabase", methods=["GET"])
@jwt_required
def dump_database():
    """
    Endpoint only available for administrators to dump the database contents

    Returns:
    Database contents in JSON format
    """

    user = User.query.get(get_jwt_identity())
    if not user.admin:
        return abort(401, description="Unauthorized.")

    return Admin.dump_database()
