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
    session,
)

import secrets

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


def do_select(
    cur_obj: sqlite3.Cursor, name: str, fields: list[str], extra_clauses: dict
):
    """
    Helper to select from a table
    """
    fields_str = ",".join(fields)
    if extra_clauses:
        where_part = " AND ".join(f"{k} = {v}" for k, v in extra_clauses.items())
        clause = f"SELECT {fields_str} FROM {name} WHERE {where_part}"
        cur_obj.execute(clause)
    else:
        cur_obj.execute(f"SELECT {fields_str} FROM {name}")

    ret = []
    for data in cur_obj.fetchall():
        data_dict = {}
        for i, name in enumerate(fields):
            data_dict[name] = data[i]

        ret.append(data_dict)

    return ret


# Define any common flask template context in this dict
template_context = {
    "canteens": {},
    "locations": {},
}

_, canteen_values = load_csv("canteens")
_, menu_values = load_csv("menu")
for canteen_id, canteen_name, canteen_description in canteen_values:
    menu = {}
    for cnt, (
        menu_canteen_id,
        item_name,
        item_is_veg,
        item_cost,
        item_img,
    ) in enumerate(menu_values, 1):
        if menu_canteen_id == canteen_id:
            menu[cnt] = {
                "name": item_name,
                "is_veg": int(item_is_veg),
                "cost": int(item_cost),
                "img": item_img,
            }

    template_context["canteens"][int(canteen_id)] = {
        "name": canteen_name,
        "description": canteen_description,
        "menu": menu,
    }

template_context["locations"] = {k: v for k, v in load_csv("locations")[1]}
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
    ("order_placer_id", "INTEGER"),
    ("order_cost", "INTEGER"),
)

USER_FIELDS = (
    ("user_phone", "INTEGER PRIMARY KEY"),
    ("user_name", "TEXT"),
    ("user_password", "TEXT"),
)

if do_reset:
    reset_table("orders", *ORDER_FIELDS)
    reset_table("user", *USER_FIELDS)
    con.commit()


con.close()

app = Flask(__name__, template_folder="src")

app.secret_key = secrets.token_urlsafe(32)


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
    return redirect("/canteens.html")


@app.route("/canteens/<int:canteen_id>/<name>")
def handle_canteens(canteen_id, name):
    if name not in ("menu", "orders") or not 1 <= canteen_id <= len(
        template_context["canteens"]
    ):
        abort(404)

    session["prev_url"] = request.path
    if "phone" not in session:
        return redirect(f"/login")

    return render_template(
        f"canteen_{name}.html", **template_context, canteen_id=canteen_id
    )


@app.route("/<name>.html")
def handle_src(name: str):
    if name not in ("canteens", "about", "orders"):
        abort(404)

    session["prev_url"] = request.path
    return render_template(name + ".html", **template_context)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        if not password:
            msg = "Password must be non-empty"

        phone = request.form.get("phone", "")
        try:
            phone = int(phone)
        except ValueError:
            msg = "Phone number should be an integer!"

        if not msg:
            con = sqlite3.connect(DB_FILE)
            try:
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM user WHERE user_phone = ? AND user_password = ?",
                    (phone, password),
                )
                if cur.fetchone():
                    session["phone"] = phone
                    return redirect(session.get("prev_url", "/index.html"))

                else:
                    msg = "Incorrect phone/password combination!"

            finally:
                con.close()

    return render_template("login.html", msg=msg)


@app.route("/logout")
def logout():
    session.pop("phone", None)
    return redirect(session.get("prev_url", "/index.html"))


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        if not password:
            msg = "Password must be non-empty"

        phone = request.form.get("phone", "")
        try:
            phone = int(phone)
        except ValueError:
            msg = "Invalid phone number (should be a non-empty number)!"

        name = request.form.get("name", "")
        if not name:
            msg = "Name must be non-empty"

        if not msg:
            con = sqlite3.connect(DB_FILE)
            try:
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM user WHERE user_phone = ?",
                    (phone,),
                )
                if cur.fetchone():
                    msg = "Account already exists!"

                else:
                    cur.execute(
                        "INSERT INTO user VALUES (?, ?, ?)",
                        (phone, name, password),
                    )
                    con.commit()
                    session["phone"] = phone
                    return redirect(session.get("prev_url", "/index.html"))

            finally:
                con.close()

    return render_template("register.html", msg=msg)


@app.route("/api/orders", methods=["GET", "POST"])
def api_orders():
    if "phone" not in session:
        abort(403)

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
                        order_dest_info,
                        order_placer_id,
                        order_cost
                    ) VALUES ('placed', ?, ?, ?, ?, ?, ?)
                """
                values = (
                    data["canteen_id"],
                    data["items"],
                    data["dest_id"],
                    data["dest_info"],
                    session["phone"],
                    data["cost"],
                )

            elif data["action"] == "accept":
                query = """
                    UPDATE orders SET order_status = 'accepted', order_deliverer_id = ?
                    WHERE order_id = ?
                    """
                values = (session["phone"], data["order_id"])

            elif data["action"] == "cancel":
                query = (
                    "UPDATE orders SET order_status = 'cancelled' WHERE order_id = ? "
                    "AND (order_deliverer_id = ? OR order_placer_id = ?)"
                )
                values = data["order_id"], session["phone"], session["phone"]

            else:
                abort(400)

            cur.execute(query, values)
            con.commit()
            return jsonify({"success": True})

        action = request.args.get("action")
        if action and action.isdigit():
            return do_select(
                cur,
                "orders",
                [
                    "order_id",
                    "order_canteen_id",
                    "order_dest_id",
                    "order_dest_info",
                    "order_cost",
                ],
                {"order_status": "'placed'", "order_canteen_id": action},
            )

        elif action in ("deliverer", "placer"):
            ret = do_select(
                cur,
                "orders",
                [i[0] for i in ORDER_FIELDS],
                {f"order_{action}_id": session["phone"]},
            )
            for d in ret:
                for change in ("placer", "deliverer"):
                    placer_id = d.get(f"order_{change}_id")
                    if placer_id:
                        ret = do_select(
                            cur, "user", ["user_name"], {"user_phone": placer_id}
                        )
                        d[f"order_{change}_name"] = ret[0]["user_name"]
                    else:
                        d[f"order_{change}_name"] = None

            return ret

        else:
            abort(400)

    except KeyError:
        abort(400)

    finally:
        con.close()


if __name__ == "__main__":
    app.run(debug=True)
