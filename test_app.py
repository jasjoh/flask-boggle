from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            # html_not_text = response.get_data()
            # print("html not text:", html_not_text)
            html = response.get_data(as_text=True)
            # print("html as text", html)
            # test that you're getting a template
            self.assertIn('id="newWordForm"', html)
            self.assertIn('<table class="board">', html)
            self.assertIn('<!-- homepage-template', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            # write a test for this route
            response = client.post("/api/new-game")
            breakpoint()
            json = response.get_data(as_text=True)
            print("json is here:", json)
            response_dict = response.get_json()




