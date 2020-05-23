from flask import Flask, render_template, request, redirect
from flask_session import Session
from tempfile import mkdtemp
from helpers import get_archives_list, parse_pgn
import requests

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
            moves_history = dict()
            for url in archives_list:
                response = requests.get(url)
                response = response.json()

                games = response["games"]

                for game in games:
                    pgn = game["pgn"]

                    parse_pgn(moves_history, pgn)

            return moves_history

        else:
            return redirect("/")


app.run(debug=True)
