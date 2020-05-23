from flask import Flask, render_template, request, redirect
from flask_session import Session
from tempfile import mkdtemp
from helpers import get_archives_list
import requests
import re

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form.get("username")

        archives_list = get_archives_list(username)

        if archives_list is not None:
            first_move_history = dict()
            for url in archives_list:
                print(url)
                response = requests.get(url)
                response = response.json()

                games = response["games"]

                for game in games:
                    pgn = game["pgn"]

                    # Find beginning of the game in the pgn
                    m = re.search(r"1\. ", pgn)
                    m2 = re.search(r" ", pgn[m.end() + 1:])

                    first_move = pgn[m.end():m.end() + m2.start() + 1]

                    if first_move in first_move_history:
                        first_move_history[first_move]["count"] += 1
                    else:
                        first_move_history[first_move] = {"count": 1}

                return first_move_history

            return {"archives": archives_list}
        else:
            return redirect("/")
