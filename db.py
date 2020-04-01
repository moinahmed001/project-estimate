from flask import Flask, escape, request
import sqlite3
from flask import _app_ctx_stack

DATABASE = 'database.db'
app = Flask(__name__)

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(DATABASE)
    return top.sqlite_db

def insert_epic(epic_issue_number, epic_title):
    query = "INSERT INTO epics (epicId, epicName) VALUES (?, ?)"
    args = (epic_issue_number, epic_title)
    database = get_db()
    database.execute(query, args)
    res =  database.commit()
    return res

def truncate_table(table_name):
    query = "DELETE FROM %s" %(table_name)
    database = get_db()
    database.execute(query)
    res =  database.commit()
    return res

def select_all_from_table(table_name):
    query = "SELECT * FROM %s" %(table_name)
    database = get_db()
    rv = database.execute(query)
    res = rv.fetchall()
    rv.close()
    print(res)
    return res


@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


#
# import click
# from flask import current_app, g
# from flask.cli import with_appcontext
#
#
# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#
#
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
