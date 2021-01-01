import random
import unittest

from src.main import create_app, db
from src.models.Track import Track


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

    def test_get_all_tracks(self):
        response = self.client.get("/tracks/")
        data_no_query = response.get_json()

        response = self.client.get("/tracks/?sortby=album")
        data_bad_query_key = response.get_json()

        response = self.client.get("/tracks/?orderby=albums")
        data_bad_query_value = response.get_json()

        response = self.client.get("/tracks/?orderby=album")
        data_orderby_album = response.get_json()

        response = self.client.get("/tracks/?orderby=artist")
        data_orderby_artist = response.get_json()

        # Check each response data set is a list and response was successful
        for data in [data_no_query, data_bad_query_key, data_bad_query_value,
                     data_orderby_album, data_orderby_artist]:
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

        # Check that bad query string keys or values return the same result as no query string
        # and that the result is different when correctly ordered by album or artist
        self.assertEqual(data_no_query, data_bad_query_key)
        self.assertEqual(data_no_query, data_bad_query_value)
        self.assertNotEqual(data_no_query, data_orderby_album)
        self.assertNotEqual(data_no_query, data_orderby_artist)
        self.assertNotEqual(data_orderby_album, data_orderby_artist)

        # Check the contents of one response to make sure everything is as expected
        for track in data_no_query:
            self.assertIsInstance(track, dict)
            self.assertIsInstance(track["album"], dict)
            self.assertEqual(len(track["album"]), 6)
            self.assertIsInstance(track["artist"], dict)
            self.assertEqual(len(track["artist"]), 5)
            self.assertIsInstance(track["disc_number"], int)
            self.assertGreaterEqual(track["disc_number"], 1)
            self.assertIsInstance(track["duration_ms"], int)
            self.assertGreaterEqual(track["duration_ms"], 1)
            self.assertIsInstance(track["explicit"], bool)
            self.assertIsInstance(track["href"], str)
            self.assertIsInstance(track["id"], int)
            self.assertIsInstance(track["is_local"], bool)
            self.assertIsInstance(track["name"], str)
            self.assertIsInstance(track["object_type"], str)
            self.assertIsInstance(track["popularity"], int)
            self.assertGreaterEqual(track["popularity"], 0)
            self.assertLessEqual(track["popularity"], 100)
            self.assertIsInstance(track["preview_url"], str)
            self.assertIsInstance(track["track_number"], int)
            self.assertGreaterEqual(track["track_number"], 1)
            self.assertIsInstance(track["uri"], str)

    def test_get_track(self):
        track = random.choice(Track.query.all())
        response = self.client.get(f"/tracks/{track.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["album"], dict)
        self.assertEqual(track.album.id, data["album"]["id"])
        self.assertIsInstance(data["artist"], dict)
        self.assertEqual(track.artist.id, data["artist"]["id"])
        self.assertEqual(track.disc_number, data["disc_number"])
        self.assertEqual(track.duration_ms, data["duration_ms"])
        self.assertEqual(track.explicit, data["explicit"])
        self.assertEqual(track.href, data["href"])
        self.assertEqual(track.id, data["id"])
        self.assertEqual(track.is_local, data["is_local"])
        self.assertEqual(track.name, data["name"])
        self.assertEqual(track.object_type, data["object_type"])
        self.assertEqual(track.popularity, data["popularity"])
        self.assertEqual(track.preview_url, data["preview_url"])
        self.assertEqual(track.track_number, data["track_number"])
        self.assertEqual(track.uri, data["uri"])
