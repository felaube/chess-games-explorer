from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import calculate_percentages, order_dict
from chess_dot_com_helpers import get_chess_dot_com_moves_history
from lichess_helpers import get_lichess_moves_history
import json
import os
import time

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
    start_whole_page = time.time()
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

        # Check if user provided a platform and an username
        if not platform:
            return render_template("index.html", error="A platform must me selected!")
        if not username:
            return render_template("index.html", error="Username not found!")

        file_path = app.config["SESSION_FILE_DIR"] + "/test_file"

        if platform == "chess_dot_com":
            
            if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                start = time.time()
                with open(file_path, 'r') as f:
                    moves_history = json.load(f)
                end = time.time()
                print(f"Time elapsed to load moves_history from file: {end-start}")

            else:
                moves_history = get_chess_dot_com_moves_history(username=username,
                                                                color=color,
                                                                rating=rating,
                                                                time_class=time_class,
                                                                time_control=time_control)
                start = time.time()
                with open(file_path, 'w') as f:
                    f.write(json.dumps(moves_history) + "\n")

                    #json.dump(moves_history, f)
                end = time.time()
                print(f"Time elapsed to save moves_history to file: {end-start}")

        if platform == "lichess":
            moves_history = get_lichess_moves_history(username=username,
                                                      color=color,
                                                      rating=rating,
                                                      time_class=time_class,
                                                      time_control=time_control)

        if moves_history is not None:
            calculate_percentages(moves_history)

            moves_history = order_dict(moves_history)

            end_whole_page = time.time()
            print(f"Time elapsed before rendering the explorer page: {end_whole_page-start_whole_page}")

            if not moves_history["next_moves"]:
                return render_template("index.html", error="No game matching selected options has been found!")

            return render_template("explorer.html",
                                   moves=json.dumps(moves_history["next_moves"]),
                                   color=color)

        else:
            return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
