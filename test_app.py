from app import app
from flask import session
from unittest import TestCase


app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# ***********************
# runs once per class
# ***********************
# @classmethod
# def setUpClass(cls):
#     print("INSIDE SET UP CLASS")

# *********************************************
# runs BEFORE and end AFTER all test have ran
# *********************************************
# @classmethod
# def tearDownClass(cls):
#     print("INSIDE TEAR DOWN CLASS")

# ********************************************
# setUP test runs BEFORE each invidual method
# ********************************************
# def setUp(self):
#     print("INSIDE SET UP")

# ********************************************
# tearDown test run AFTER each invidual method
# ********************************************
# def tearDown(self):
#     print("INSIDE TEAR DOWN")


# ***************************************************************************
# TEST get request that checks status code 200 and check header in index.html
# ***************************************************************************
class HashtagViewsTestCase(TestCase):
    def test_hashtag_form(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h3>Add your text here for hashtag results</h3>", html)

    # ***************************************************************************
    # TEST get request that checks status code 200 and check header in index.html
    # ***************************************************************************
    def test_hashtag_submit(self):
        with app.test_client() as client:
            res = client.get("/hashtagsuggestion?hashtag=apple")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h3>Hashtag: music</h3>", html)

    # *****************************************************
    # TEST redirect RESPONSE and getting status code of 302
    # *****************************************************
    def test_redirection(self):
        with app.test_client() as client:
            res = client.get("/logout")

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    # ************************************************************************
    # TEST redirection FOLLOWED and getting status code of 200 and header from html
    # ************************************************************************
    def test_redirection_followed(self):
        with app.test_client() as client:
            res = client.get("/logout", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h3>Add your text here for hashtag results</h3>", html)

    # **********************************
    # TEST session count to set if to 1
    # **********************************
    def test_session_count(self):
        with app.test_client() as client:
            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session["count"], 1)

    # ******************************************
    # TEST session count if it will set to 1000
    # *****************************************
    def test_session_count_set(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["count"] = 999

            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session["count"], 1000)
