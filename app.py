from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
db = sqlite3.connect("movies.db")
cursor = db.cursor()


@app.route("/", methods=["GET", "POST"])
def home():
    # return "Hello, Flask!"
    # return "<h1>Jestem na stronie domowej<br><a href='addMovie'>Idź do strony dodawania</a>"
    # return render_template("home.html", movies=LISTA_FILMÓW)
    if request.method == "POST":
        movies_to_remove_ids = request.form.getlist("movieToRemove")
        with sqlite3.connect("movies.db") as con:
            cursor = con.cursor()
            for movie_id in movies_to_remove_ids:
                cursor.execute(f"DELETE FROM movies WHERE ID={movie_id}")
            con.commit()

    with sqlite3.connect("movies.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM movies")
        moviesList = cursor.fetchall()
    return render_template("home.html", movies=moviesList)


# @app.route("/addMovie")
@app.route("/addMovie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movieTitle = request.form.get("title")
        movieYear = request.form.get("year")
        movieActors = request.form.get("actors")

        with sqlite3.connect("movies.db") as con:
            cursor = con.cursor()
            cursor.execute(
                f'INSERT INTO movies (title, year, actors) VALUES ("{movieTitle}",{movieYear},"{movieActors}")'
            )
            con.commit()
        return redirect(url_for("home"))

    # return "<br>Jestem na stronie dodawania nowego filmu</br><a href='/'>Powrót do strony domowej"
    return render_template("add.html")


@app.route("/calculate")
def calculate():
    op = request.args.get("op", type=str)
    arg1 = request.args.get("arg1", type=int)
    arg2 = request.args.get("arg2", type=int)

    if op == "sum":
        output = arg1 + arg2
        # return f"suma wynosi: {arg1 + arg2}"
        return f"{arg1} + {arg2} = {output}"
    elif op == "multiply":
        output = arg1 * arg2
        return f"{arg1} * {arg2} = {output}"
    else:
        return "Nie ma takiej operacji"
    # return f"Wynik to: {str(output)}"


if __name__ == "__main__":
    app.run(debug=True)
