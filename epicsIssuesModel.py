import requests, json
import db
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def get_epic_issues(board_name, epic_number):
    query = "SELECT * from epicsIssues where epicId=%s AND boardName='%s'" %(epic_number, board_name)
    all_epics_issues = db.with_query(query)
    return loop_all_epics_issues(all_epics_issues)

def get_epics_issues():
    all_epics_issues = db.select_all_from_table("epicsIssues")
    return loop_all_epics_issues(all_epics_issues)

def loop_all_epics_issues(all_epics_issues):
    array_epics_issues = {'epicsIssues':[]}
    for epics_issue in all_epics_issues:
        array_epics_issues["epicsIssues"].append({
            "epicsIssueId": epics_issue[0],
            "epicId": epics_issue[1],
            "issueNumber": epics_issue[2],
            "boardName": epics_issue[3]
        })
    return array_epics_issues

def fetch_epic_issues(epicId):
    zenhub_root_url = app.config['ZENHUB_ROOT_URL']
    epics_url = app.config['EPICS_URL']
    epics_url = epics_url.replace("{repositories_id}", app.config['REPOSITORIES_ID'])

    headers = {'X-Authentication-Token': app.config['ZENHUB_AUTH_TOKEN']}
    url = zenhub_root_url + epics_url + "/" + str(epicId)

    r = requests.get(url, headers=headers)

    data = r.json()
    return data

def insert_epics_issues(epic_id, issue_number, board_name):
    query = "INSERT INTO epicsIssues (epicId, issueNumber, boardName) VALUES (?, ?, ?)"
    args = (epic_id, issue_number, board_name)
    return db.insert_query(query, args)

def delete_all_epics_issues_for_board():
    delete_epicsIssues_query = "DELETE FROM epicsIssues where boardName = '%s'" %(app.config['REPOS'])
    return db.with_query(delete_epicsIssues_query)
