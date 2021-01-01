import random
import unittest

from flask_jwt_extended import create_access_token

from src.main import create_app, db
from src.models.User import User


class TestProfiles(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "drop"])
        cls.app_context.pop()

    def test_get_user(self):
        user = random.choice(User.query.all())
        access_token = create_access_token(identity=str(user.id))
        response = self.client.get(
            "/me",
            headers={
                "Authorization": f"Bearer {access_token}"
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(user.admin, data["admin"])
        self.assertEqual(user.country, data["country"])
        self.assertEqual(user.display_name, data["display_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.href, data["href"])
        self.assertEqual(user.id, data["id"])
        self.assertEqual(user.object_type, data["object_type"])
        self.assertEqual(user.product, data["product"])
        self.assertEqual(user.uri, data["uri"])
