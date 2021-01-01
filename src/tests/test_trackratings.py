import random
import unittest

from flask_jwt_extended import create_access_token

from src.main import create_app, db
from src.models.Track import Track
from src.models.TrackRating import Track_Rating
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

    def test_trackrating_create(self):
        # Use admin user as they should not have any track ratings
        user = User.query.filter_by(admin=True).first()
        track = random.choice(Track.query.all())
        rating = random.randint(1, 5)
        access_token = create_access_token(identity=str(user.id))
        response = self.client.post(
            f"/me/trackratings/{track.id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "rating": rating
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["rating"], int)
        self.assertEqual(data["rating"], rating)

        # Check bad rating input
        response = self.client.post(
            f"/me/trackratings/{track.id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "rating": 6
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 400)

        # Check track rating exists
        trackrating = random.choice(Track_Rating.query.all())
        rating = random.randint(1, 5)
        access_token = create_access_token(identity=str(trackrating.user_id))
        response = self.client.post(
            f"/me/trackratings/{trackrating.track_id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "rating": rating
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 400)

    def test_trackrating_get(self):
        trackrating = random.choice(Track_Rating.query.all())
        access_token = create_access_token(identity=str(trackrating.user_id))
        response = self.client.get(
            f"/me/trackratings/{trackrating.track_id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["rating"], int)
        self.assertEqual(data["rating"], trackrating.rating)
        self.assertIsInstance(data["track"], dict)
        self.assertIsInstance(data["track_id"], int)
        self.assertEqual(data["track_id"], trackrating.track_id)
        self.assertIsInstance(data["user_id"], int)
        self.assertEqual(data["user_id"], trackrating.user_id)

    def test_trackrating_update(self):
        trackrating = random.choice(Track_Rating.query.all())

        # Get random rating that is different to the current rating
        ratings = [1, 2, 3, 4, 5]
        ratings.remove(trackrating.rating)
        rating = random.choice(ratings)

        access_token = create_access_token(identity=str(trackrating.user_id))
        response = self.client.put(
            f"/me/trackratings/{trackrating.track_id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "rating": rating
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["rating"], int)
        self.assertEqual(data["rating"], rating)
        self.assertIsInstance(data["track"], dict)
        self.assertIsInstance(data["track_id"], int)
        self.assertEqual(data["track_id"], trackrating.track_id)
        self.assertIsInstance(data["user_id"], int)
        self.assertEqual(data["user_id"], trackrating.user_id)

    def test_trackrating_delete(self):
        trackrating = random.choice(Track_Rating.query.all())
        access_token = create_access_token(identity=str(trackrating.user_id))
        response = self.client.delete(
            f"/me/trackratings/{trackrating.track_id}",
            headers={
                "Authorization": f"Bearer {access_token}"
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, str)
        self.assertFalse(Track_Rating.query.filter_by(user_id=trackrating.user_id, track_id=trackrating.track_id).first())
