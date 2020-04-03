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

def select_all_from_table(table_name):
    query = "SELECT * FROM %s" %(table_name)
    database = get_db()
    rv = database.execute(query)
    res = rv.fetchall()
    rv.close()
    return res

def insert_query(query, args):
    database = get_db()
    database.execute(query, args)
    res =  database.commit()
    return res

def with_query(query):
    database = get_db()
    rv = database.execute(query)
    res = rv.fetchall()
    rv.close()
    return res


@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()
