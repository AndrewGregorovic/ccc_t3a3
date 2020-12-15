from flask import abort, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from src.models.Admin import Admin
from src.models.User import User


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/dumpdatabase", methods=["GET"])
@jwt_required
@verify_jwt_in_request
def dump_database():
    user = User.query.get(get_jwt_identity())
    if not user.admin:
        return abort(401, description="Unauthorized.")

    return jsonify(Admin.dump_database())
