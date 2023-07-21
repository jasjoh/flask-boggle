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
            # write a test for this route
            # check if game is a game
            # check if board is filled
            response = client.post("/api/new-game")
            response_dict = response.get_json()
            board_length = len(response_dict.get("board"))
            print("games:", games)

            # check if board exists and is an iterable with a length > 0
            self.assertTrue(board_length > 0)

            # check that game ID is valid
            self.assertTrue(games.get(response_dict.get("gameId")))

    def test_api_score_word(self):
        """Test scoring a word."""

        with self.client as client:
            # create a game
            response = client.post("/api/new-game")
            response_dict = response.get_json()

            # get the game and overwrite the board
            game_id = response_dict.get("gameId")
            our_game = games[game_id]
            print("our game board:", our_game.board)
            # this has to be 3 x 3 (1 x 3 doesn't work)
            our_game.board = [['C', 'A', 'T'],['C', 'A', 'T'],['C', 'A', 'T']]

            # call score_word with CAT and get {result: "ok"}
            # format of POST to endpoint expecting JSON is 'json={}', not 'data={}'
            response = client.post(
                "/api/score-word",
                json={"game_id": game_id, "word": "CAT"}
            )
            print("score word response", response)
            response_dict = response.get_json()
            print("score word response dict:", response_dict)
            self.assertTrue(response_dict == {"result": "ok"})

            # call score_word with FOOBAR and get {result: "not-word"}
            # call score_word with DOG and get {result: "not-on-board"}

            ...




