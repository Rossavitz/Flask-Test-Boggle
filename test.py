from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
        app.config["SECRET_KEY"] = "duck-moose-cricket"

    def test_boggle_load(self):
        """test page load"""
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 200)

    def test_not_on_board(self):
        """test if valid word but not on board"""
        with app.test_client() as client:

            client.get("/")
            resp = client.get("/result?word=hypothetical")
            self.assertEqual(resp.json["result"], "not-on-board")

    def test_not_word(self):
        """test if valid word"""
        with app.test_client() as client:

            client.get("/")
            resp = client.get("/result?word=kdjfalkjgfhg")
            self.assertEqual(resp.json["result"], "not-word")

    def test_session_info(self):
        """update and test highScore/timesPlayed"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["highScore"] = 900
                change_session["timesPlayed"] = 500

            client.post("/end-game")

            self.assertEqual(session["highScore"], 900)
            self.assertEqual(session["timesPlayed"], 500)

    def test_session_score(self):
        """update and test highScore/timesPlayed"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["score"] = 100

            client.get("/")

            self.assertEqual(session["score"], 100)
