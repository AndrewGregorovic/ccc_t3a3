from datetime import timedelta

from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from src.main import bcrypt, db
from src.models.User import User
from src.schemas.UserSchema import user_register_schema, user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def auth_register():
    """
    Creates a new user in the app

    Returns:
    Tuple containing the dict of the new user and status code
    """

    user_fields = user_register_schema.load(request.json)

    # Check uniqueness of email and return abort instead of getting errors
    if User.query.filter_by(email=user_fields["email"]).first():
        return abort(400, description="Email already registered.")

    user = User()
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    # Need to retrieve the user after adding to the database so that the href and uri fields
    # can be updated with the correct user id
    users = User.query.filter_by(email=user_fields["email"])

    # Need to remove password from user_fields otherwise it will replace the password hash with
    # the clear text password entered by the user to register
    del user_fields["password"]
    user_fields["href"] = f"https://api.spotify.com/user/{users[0].id}"
    user_fields["uri"] = f"spotify:user:{users[0].id}"

    users.update(user_fields)
    db.session.commit()

    return (jsonify(user_schema.dump(user)), 201)


@auth.route("/login", methods=["POST"])
def auth_login():
    """
    Logs the user in using email/password and returns a JWT for authorization to use other endpoints

    Returns:
    Dict containing the JWT for the user
    """

    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect email and password.")

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    return jsonify({"token": access_token})
