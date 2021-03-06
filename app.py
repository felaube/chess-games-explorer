from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import calculate_percentages, order_dict
from chess_dot_com_helpers import get_chess_dot_com_moves_history
from lichess_helpers import get_lichess_moves_history
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
        platform = request.form.get("platform")
        color = request.form.get("color")
        rating = request.form.get("rating")
        time_class = request.form.get("time_class")
        time_control = request.form.get("time_control")

        # If user did not provide a username or a platform,
        # redirect to home page
        if not username or not platform:
            return redirect("/")

        if platform == "chess_dot_com":
            moves_history = get_chess_dot_com_moves_history(username=username,
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

        if moves_history is not None:
            calculate_percentages(moves_history)

            moves_history = order_dict(moves_history)

            return render_template("explorer.html",
                                   moves=json.dumps(moves_history["next_moves"]),
                                   color=color)

        else:
            return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
