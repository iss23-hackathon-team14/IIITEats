from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    abort,
    jsonify,
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


def load_csv(name: str):
    """
    Helper to load a CSV file
    """
    file = CONFIG_DIR / f"{name}.csv"

    head = ()
    data = []
    if file.exists():
        with open(file) as f:
            for row in csv.reader(f):
                if not head:
                    head = tuple(row)
                else:
                    if len(row) != len(head):
                        raise RuntimeError(f"Row '{row}' has incorrect width")

                    data.append(row)

    return head, data


def load_csv_as_dict(name: str):
    """
    Helper to load csv as a list of dict objects
    """
    head, data = load_csv(name)
    ret = []
    for elem in data:
        dict_elem = {}
        for i, fname in enumerate(head):
            dict_elem[fname] = elem[i]
        ret.append(dict_elem)

    return ret


def populate_table_from_csv(name: str):
    """
    Populates table called 'name' from a csv file stored in 'CONFIG_DIR' (if it exists)
    """
    head, data = load_csv(name)
    if not head:
        return

    head_str = ",".join(head)
    values_param = ",".join(["?"] * len(head))
    cur.executemany(f"INSERT INTO {name} ({head_str}) VALUES({values_param})", data)


def reset_table(name: str, *params: tuple[str, str]):
    """
    Initialise a table given by 'name' with the params passed.
    """
    cur.execute(f"DROP TABLE IF EXISTS {name}")
    cur.execute(f"CREATE TABLE {name}({','.join(' '.join(i) for i in params)})")
    populate_table_from_csv(name)


def do_select(cur_obj: sqlite3.Cursor, name: str, fields: list[str]):
    """
    Helper to select from a table
    """
    fields_str = ",".join(fields)
    cur_obj.execute(f"SELECT {fields_str} FROM {name}")
    ret = []
    for data in cur_obj.fetchall():
        data_dict = {}
        for i, name in enumerate(fields):
            data_dict[name] = data[i]

        ret.append(data_dict)

    return ret


# Define any common flask template context in this dict
template_context = {i: load_csv_as_dict(i) for i in ("menu", "canteens", "locations")}

do_reset = not DB_FILE.exists()
con = sqlite3.connect(DB_FILE)
cur = con.cursor()


ORDER_FIELDS = (
    ("order_id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("order_status", "TEXT"),
    ("order_canteen_id", "INTEGER"),
    ("order_items", "TEXT"),
    ("order_dest_id", "INTEGER"),
    ("order_dest_info", "TEXT"),
    ("order_deliverer_id", "INTEGER"),
)

USER_FIELDS = (
    ("user_id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("user_name", "TEXT"),
    ("user_phone", "TEXT"),
)
if do_reset:
    reset_table("orders", *ORDER_FIELDS)
    reset_table("user", *USER_FIELDS)
    con.commit()


con.close()

app = Flask(__name__, template_folder="src")


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


@app.route("/canteens/<int:canteen_id>.html")
def handle_canteens(canteen_id):
    return render_template("canteen.html", **template_context, canteen_id=canteen_id)


@app.route("/<name>.html")
def handle_src(name: str):
    return render_template(name + ".html", **template_context)


@app.route("/api/orders", methods=["GET", "POST"])
def api_place_order():
    con = sqlite3.connect(DB_FILE)
    try:
        cur = con.cursor()
        if request.method == "POST":
            data = request.json
            if data is None:
                abort(400)

            if data["action"] == "place":
                query = """
                    INSERT INTO orders (
                        order_status,
                        order_canteen_id,
                        order_items,
                        order_dest_id,
                        order_dest_info
                    ) VALUES ('placed', ?, ?, ?, ?)
                """
                values = (
                    data["canteen_id"],
                    data["items"],
                    data["dest_id"],
                    data["dest_info"],
                )

            elif data["action"] == "accept":
                query = """
                    UPDATE orders SET order_status = 'accepted', order_deliverer_id = ?
                    WHERE order_id = ?
                    """
                values = (data["deliverer_id"], data["order_id"])

            elif data["action"] == "set_status":
                query = "UPDATE orders SET order_status = ? WHERE order_id = ?"
                values = (data["status"], data["order_id"])

            else:
                abort(400)

            cur.execute(query, values)
            con.commit()
            return jsonify({"success": True})

        return do_select(cur, "orders", [i[0] for i in ORDER_FIELDS])

    except KeyError:
        abort(400)

    finally:
        con.close()


if __name__ == "__main__":
    app.run()
