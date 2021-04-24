"""
Implements the rendering of templates and the input parsing
"""
import json
from tempfile import mkdtemp
from flask import Flask, render_template, request, session
from flask_session import Session
from helpers import calculate_percentages, order_dict
from chess_dot_com_helpers import get_chess_dot_com_moves_history
from lichess_helpers import get_lichess_moves_history

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
    """
    Render the correct form of index.html depending on the request
    """
    if request.method == "GET":
        session.clear()
        # Render home page
        return render_template("index.html")

    if request.method == "POST":
        # Get information from form
        username = request.form.get("username")
        platform = request.form.get("platform")
        color = request.form.get("color")
        rating = request.form.get("rating")
        time_class = request.form.get("time_class")
        time_control = request.form.get("time_control")

        # Treat rating input
        if rating == "":
            rating = None
        else:
            rating = int(rating)

        # Check if user provided a platform and an username
        if not platform:
            return render_template("index.html", error="A platform must be selected!")
        if not username:
            return render_template("index.html", error="A username must be provided!")

        # Obtain player's moves history
        if platform == "chess_dot_com":
            moves_history = get_chess_dot_com_moves_history(username=username.lower(),
                                                            color=color,
                                                            rating=rating,
                                                            time_class=time_class,
                                                            time_control=time_control)

        if platform == "lichess":
            moves_history = get_lichess_moves_history(username=username,
                                                      color=color,
                                                      rating=rating,
                                                      time_class=time_class,
                                                      time_control=time_control)

        # Validate moves_history
        if moves_history is None:
            return render_template("index.html", error="Username not found!")

        if not moves_history["next_moves"]:
            return render_template("index.html", error="No games matching the selected"
                                                        " options have been found!")

        # Set up and render the explorer
        calculate_percentages(moves_history)

        moves_history = order_dict(moves_history)

        return render_template("explorer.html",
                                moves=json.dumps(moves_history["next_moves"]),
                                color=color)


if __name__ == "__main__":
    app.run()
