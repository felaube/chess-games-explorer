from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import get_archives_list, parse_pgn, calculate_percentages, order_dict
import requests
import json

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        session.clear()
        # Render home page
        return render_template("index.html")
    if request.method == "POST":
        # Get information from form and set up the explorer
        username = request.form.get("username")

        archives_list = get_archives_list(username)

        if archives_list is not None:
            moves_history = {"next_moves": {}}
            for url in archives_list:
                response = requests.get(url)
                response = response.json()

                games = response["games"]

                for game in games:

                    # Don't consider chess variations
                    # other than the classical one
                    if game["rules"] == "chess":

                        # Apply filters
                        # Filter by color
                        if game[request.form.get("color")]["username"] == username:

                            # Filter by rating
                            if request.form.get("rating"):
                                if int(game[request.form.get("color")]["rating"]) < int(request.form.get("rating")):
                                    continue

                            # Filter by time class
                            if request.form.get("time_class"):
                                if game["time_class"] != request.form.get("time_class"):
                                    continue

                            # Filter by time control
                            if request.form.get("time_control"):
                                if game["time_control"] != request.form.get("time_control"):
                                    continue

                            # Parse each game from the archive
                            try:
                                pgn = game["pgn"]

                                parse_pgn(moves_history, pgn)
                            except KeyError:
                                pass

            calculate_percentages(moves_history)

            moves_history = order_dict(moves_history)

            return render_template("explorer.html", moves=json.dumps(moves_history["next_moves"]), color=request.form.get("color"))

        else:
            return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
