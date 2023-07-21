from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {} # {game_id: game_object_instance}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return {"gameId": "need-real-id", "board": "need-real-board"}

@app.post("/api/score-word")
def score_word():
    # accept post with JSON including game ID and the word
    json = request.json # assumption: json is a Dict{}
    # print("json is:", json)
    game_id = json["game_id"]
    word = json["word"]
    # should check if word is legal
    # -- it should be in word list
    is_in_list = games[game_id].is_word_in_word_list(word)
    print("is in list?:", is_in_list)
    # -- it should be findable on the board
    is_findable = games[game_id].check_word_on_board(word)
    print("is findable?:", is_findable)
    # if not a word: {result: "not-word"}
    if not is_in_list:
        return jsonify({"result": "not-word"})
    # if not on board: {result: "not-on-board"}
    if not is_findable:
        return jsonify({"result": "not-on-board"})
    # if a valid word: {result: "ok"}
    return jsonify({"result": "ok"})
