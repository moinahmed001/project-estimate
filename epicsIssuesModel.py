import requests, json
import time
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

def get_issue_epic(board_name, issue_number):
    query = "SELECT * from epicsIssues where issueNumber=%s AND boardName='%s'" %(issue_number, board_name)
    all_epics_issues = db.with_query(query)

    return loop_all_epics_issues(all_epics_issues)

def get_epic_issues_full_details(board_name, epic_number):
    query = "SELECT ei.issueNumber, i.title from epicsIssues as ei JOIN issues as i on ei.issueNumber = i.issueNumber WHERE ei.epicId=%s AND ei.boardName='%s'" %(epic_number, board_name)
    all_epics_issues = db.with_query(query)

    array_epics_issues = {'epicsIssues':[]}
    for epics_issue in all_epics_issues:
        array_epics_issues["epicsIssues"].append({
            "issueNumber": epics_issue[0],
            "title": epics_issue[1]
        });

    return array_epics_issues

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

def fetch_epic_issues(epicId, repoId):
    zenhub_root_url = app.config['ZENHUB_ROOT_URL']
    epics_url = app.config['EPICS_URL']
    epics_url = epics_url.replace("{repositories_id}", str(repoId))

    headers = {'X-Authentication-Token': app.config['ZENHUB_AUTH_TOKEN']}
    url = zenhub_root_url + epics_url + "/" + str(epicId)

    print("Attempting to fetch epic issues url: %s" %(url))
    r = requests.get(url, headers=headers)
    print("Zenhub api rate used so far %s out 100" %(r.headers["X-RateLimit-Used"]))

    if int(r.headers["X-RateLimit-Used"]) > 95:
        sleep_for = (int(r.headers["X-RateLimit-Reset"]) - int(time.time())) + 1
        print("SLEEPING FOR %s seconds" %(sleep_for))
        time.sleep(sleep_for)
    data = r.json()
    return data

def insert_epics_issues(epic_id, issue_number, board_name):
    query = "INSERT INTO epicsIssues (epicId, issueNumber, boardName) VALUES (?, ?, ?)"
    args = (epic_id, issue_number, board_name)
    return db.insert_query(query, args)

def delete_all_epics_issues_for_board(board_name):
    delete_epicsIssues_query = "DELETE FROM epicsIssues where boardName = '%s'" %(board_name)
    return db.delete_query(delete_epicsIssues_query)
