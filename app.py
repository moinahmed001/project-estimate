from flask import Flask, escape, request
import db



app = Flask(__name__)


@app.route('/')
def hello():
    for user in query_db('select * from users'):
        print(user['username'], 'has the id', user['user_id'])

    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

def query_db(query, args=(), one=False):
    cur = db.get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/ingest/epics')
def ingestEpics():
    return 'done'

@app.route('/ingest/issues')
def ingestIssues():
    return 'done'
