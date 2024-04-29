from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "duck-moose-cricket"

boggle_game = Boggle()


@app.route("/")
def gen_board():
    """Generate a boggle board"""
    board = boggle_game.make_board()
    session["board"] = board
    highScore = session.get("highScore", 0)
    timesPlayed = session.get("timesPlayed", 0)
    return render_template(
        "root.html", board=board, highScore=highScore, timesPlayed=timesPlayed
    )


@app.route("/result")
def verify_word():
    """check if word is valid"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({"result": response})


@app.route("/score", methods=["POST"])
def score():
    """Get score and post to page"""
    score = request.json["score"]
    return jsonify(score)


@app.route("/end-game", methods=["POST"])
def end_game():
    """End game and get the score"""
    score = request.json["total"]
    highScore = session.get("highScore", 0)
    timesPlayed = session.get("timesPlayed", 0)

    session["timesPlayed"] = timesPlayed + 1
    session["highScore"] = max(score, highScore)

    return jsonify(newHighScore=score > highScore)
