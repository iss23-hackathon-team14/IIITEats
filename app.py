from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
)

# source directory. Also used as flask templates
SRC = "src"

# base directory of project
BASE_DIR = Path(".")


# Directory where all config data is stored
CONFIG_DIR = BASE_DIR / "config"

# path to sqlite3 db file
DB_FILE = BASE_DIR / "database.db"


def populate_table_from_csv(name: str):
    """
    Populates a table called 'name' from a csv file stored in 'CONFIG_DIR'
    """
    file = CONFIG_DIR / f"{name}.csv"
    if not file.exists():
        return

    head = ""
    data: list[list[str]] = []
    col_width = 0
    with open(file) as f:
        for row in csv.reader(f):
            if not head:
                head = ", ".join(row)
                col_width = len(row)
            else:
                if len(row) != col_width:
                    raise RuntimeError(f"Row '{row}' has incorrect width")

                data.append(row)

    cur.executemany(
        f"INSERT INTO {name}({head}) VALUES({','.join(['?'] * col_width)})", data
    )


def reset_table(name: str, *params: tuple[str, str]):
    """
    Initialise a table given by 'name' with the params passed.
    """
    cur.execute(f"DROP TABLE IF EXISTS {name}")
    cur.execute(f"CREATE TABLE {name}({','.join(' '.join(i) for i in params)})")
    populate_table_from_csv(name)


con = sqlite3.connect(DB_FILE)
cur = con.cursor()

# Do any init db stuff here


con.close()

app = Flask(__name__, template_folder="src")

# Define any common flask template context in this dict
template_context = {}


@app.route("/images/<path:path>")
def send_images(path: str):
    return send_from_directory("images", path)


@app.route("/fonts/<path:path>")
def send_fonts(path: str):
    return send_from_directory("fonts", path)


@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory(".", "favicon.ico")


@app.route("/css/<name>.css")
def send_css(name: str):
    return send_from_directory("src/css", name + ".css")


@app.route("/scripts/<name>.js")
def send_js(name: str):
    return send_from_directory("src/scripts", name + ".js")


@app.route("/")
def send_index():
    return redirect("/index.html")


@app.route("/<name>.html")
def handle_src(name: str):
    return render_template(name + ".html", **template_context)


if __name__ == "__main__":
    app.run()
