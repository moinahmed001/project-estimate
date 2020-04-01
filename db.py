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

def insert_epics(epic_issue_number, epic_title):
    query = "INSERT INTO epics (epicId, epicName) VALUES (?, ?)"
    args = (epic_issue_number, epic_title)
    database = get_db()
    database.execute(query, args)
    res =  database.commit()
    return res

def insert_epics_issues(epic_id, issue_number):
    query = "INSERT INTO epicsIssues (epicId, issueNumber) VALUES (?, ?)"
    args = (epic_id, issue_number)
    database = get_db()
    database.execute(query, args)
    res =  database.commit()
    return res

def insert_issues(issue_number, board_name, title, issue_status, issue_link):
    query = "INSERT INTO issues (issueNumber, boardName, title, issueStatus, issueLink) VALUES (?, ?, ?, ?, ?)"
    args = (issue_number, board_name, title, issue_status, issue_link)
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
    return res


@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()
