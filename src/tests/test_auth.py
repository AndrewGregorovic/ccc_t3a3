import random
import unittest

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
        db.drop_all()
        cls.app_context.pop()

    def test_user_register(self):
        response = self.client.post(
            "/auth/register",
            json={
                "email": "unittest99@test.com",
                "password": "123456"
            })
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["email"], "unittest99@test.com")

    def test_user_login(self):
        user = random.choice(User.query.filter_by(admin=False).all())
        response = self.client.post(
            "/auth/login",
            json={
                "email": user.email,
                "password": "123456"
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(data['token'], str)
