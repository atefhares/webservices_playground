import flask
import sqlite3
from flask import g
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATABASE = './database.db'

TABLE_NAME = "books"
COLUMN_ID_NAME = "id"
COLUMN_TITLE_NAME = "title"
COLUMN_AUTHOR_NAME = "author"
COLUMN_CATEGORY_NAME = "category"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_db_tables_if_not_exists():
    cur = get_db().cursor()
    cur.execute(
        "create table if not exists " + TABLE_NAME + " ("
        + COLUMN_ID_NAME + " INTEGER " + " PRIMARY KEY AUTOINCREMENT, "
        + COLUMN_TITLE_NAME + " TEXT " + " NOT NULL, "
        + COLUMN_AUTHOR_NAME + " TEXT " + " NOT NULL, "
        + COLUMN_CATEGORY_NAME + " TEXT " + " NOT NULL "
        + ") "
    )


@app.route('/', methods=['GET'])
def home():
    return "<h1>This is a home test</h1>"


@app.route('/books', methods=['GET'])
def list_books():
    create_db_tables_if_not_exists()
    cur = get_db().cursor()
    all_books = cur.execute("select * from " + TABLE_NAME).fetchall()
    print(all_books)
    if len(all_books) > 0:
        return jsonify(all_books)
    else:
        return "<h1>No books found</h1>"


@app.route('/books', methods=['POST'])
def create_book():
    print(request.form)

    create_db_tables_if_not_exists()
    cur = get_db().cursor()

    query_state = "insert into " + TABLE_NAME + "(" + COLUMN_TITLE_NAME + "," + COLUMN_AUTHOR_NAME
    query_state += "," + COLUMN_CATEGORY_NAME + ")"
    query_state += " values(" + "\'" + request.form["t"]
    query_state += "\'" + "," + "\'" + request.form["a"] + "\'"
    query_state += "," + "\'" + request.form["c"] + "\'" + ");"

    print("Stat: ", query_state)
    cur.execute(query_state)
    get_db().commit()

    book = cur.execute(
        "SELECT * from " + TABLE_NAME + " where " + COLUMN_ID_NAME + " =last_insert_rowid()"
    ).fetchone()

    return jsonify(book)


@app.route('/books/<int:id>', methods=['GET'])
def show_book(id):
    print(id)
    cur = get_db().cursor()
    book = cur.execute(
        "SELECT * from " + TABLE_NAME + " where " + COLUMN_ID_NAME + "=" + str(id)
    ).fetchone()
    return jsonify(book)


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    print(id)
    cur = get_db().cursor()
    cur.execute(
        "delete from " + TABLE_NAME + " where " + COLUMN_ID_NAME + "=" + str(id)
    )
    get_db().commit()
    return "Effected rows: " + str(cur.rowcount)


@app.route('/books/<int:id>', methods=['PUT', 'PATCH'])
def update_book(id):
    print("REQUEST: ", id)
    cur = get_db().cursor()

    data = (
        request.form["t"],
        request.form["a"],
        request.form["c"],
        str(id),
    )

    sql_stat = "UPDATE " + TABLE_NAME
    sql_stat += " SET "
    sql_stat += "\'" + COLUMN_TITLE_NAME + "\'" + " = ?, "
    sql_stat += "\'" + COLUMN_AUTHOR_NAME + "\'" + " = ?, "
    sql_stat += "\'" + COLUMN_CATEGORY_NAME + "\'" + " = ? "
    sql_stat += " WHERE " + COLUMN_ID_NAME + " = ?"
    sql_stat += ";"

    print("SQL: ", sql_stat)
    print("data: ", data)
    cur.execute(sql_stat, data)
    get_db().commit()

    return "Effected rows: " + str(cur.rowcount)


app.run()
