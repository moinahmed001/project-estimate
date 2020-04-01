from flask import Flask, escape, request
import db
import epics, issues
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def hello():
    # for user in query_db('select * from users'):
        # print(user['username'], 'has the id', user['user_id'])

    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/api/epics')
def api_epics():
    return jsonify(epics.get_epics())

@app.route('/api/issue/<issue_number>')
def api_issue(issue_number):
    return issues.fetch_issue(issue_number)

def query_db(query, args=(), one=False):
    cur = db.get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/ingest/epics')
def api_ingest_epics():
    # Get all the epics
    all_epics = epics.fetch_epics()

    epic_issues = all_epics['epic_issues']
    # print(issues)
    db.truncate_table('epics')
    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issues.fetch_issue(epic_issue_number)
        db.insert_epic(epic_issue_number, epic_issue_details['title'])

    # i=0
    # while(i<len(issues)):
    #     print(">>>>> ")
    #     print(issues[i])
    #     i+=1
    return "issues"


@app.route('/api/ingest/issues')
def api_ingest_issues():
    return 'done'
