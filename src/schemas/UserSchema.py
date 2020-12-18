from marshmallow.validate import Equal, Length, OneOf

from src.main import ma
from src.models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]
        dump_only = ["admin"]

    email = ma.String(required=True, validate=Length(min=4))
    password = ma.String(required=True, validate=Length(min=6))
    country = ma.String(validate=Length(equal=2))
    display_name = ma.String(validate=Length(max=30))
    href = ma.String()
    product = ma.String(validate=[
        Length(max=20),
        OneOf(["free", "premium", "student"])
    ])
    object_type = ma.String(validate=Equal("user"))
    uri = ma.String()
    admin = ma.Boolean()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Separate schema for loading json on user register to only accept the fields required to register
user_register_schema = UserSchema(only=("email", "password"))
