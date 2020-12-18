from flask import abort, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.main import db
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


@admin.route("/product_numbers", methods=["GET"])
@jwt_required
def get_product_numbers():
    """
    Endpoint only available for administrators to view the number of users with each product

    Returns:
    Dict of the product type and number of users for each product type
    """

    user = User.query.get(get_jwt_identity())
    if not user.admin:
        return abort(401, description="Unauthorized.")

    product_numbers = User.query\
        .with_entities(User.product, db.func.count(User.product))\
        .group_by(User.product).all()

    return jsonify([dict(zip(("product_type", "users"), product)) for product in product_numbers])
