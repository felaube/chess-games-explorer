from flask import Flask, render_template, request
from flask_session import Session
from tempfile import mkdtemp
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

        # Get array of monthly archives available for this player
        archives = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
        print(archives)
