import requests, json
import db
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def fetch_issue(issue_number):
    github_root_url = app.config['GITHUB_ROOT_URL']
    issue_url = app.config['GITHUB_ISSUE_URL']
    issue_url = issue_url.replace("{github_organisation_name}", app.config['GITHUB_ORGANISATION_NAME'])
    issue_url = issue_url.replace("{repos}", app.config['REPOS'])
    issue_url = issue_url.replace("{issue_number}", str(issue_number))

    headers = {'Accept': app.config['GITHUB_ACCEPT_HEADER'], 'Authorization': app.config['GITHUB_AUTH_TOKEN']}
    url = github_root_url + issue_url

    r = requests.get(url, headers=headers)

    data = r.json()
    return data


def get_issue_from_github(board_name, issue_number):
    github_root_url = app.config['GITHUB_ROOT_URL']
    issue_url = app.config['GITHUB_ISSUE_URL']
    issue_url = issue_url.replace("{github_organisation_name}", app.config['GITHUB_ORGANISATION_NAME'])
    issue_url = issue_url.replace("{repos}", board_name)
    issue_url = issue_url.replace("{issue_number}", str(issue_number))

    headers = {'Accept': app.config['GITHUB_ACCEPT_HEADER'], 'Authorization': app.config['GITHUB_AUTH_TOKEN']}
    url = github_root_url + issue_url

    r = requests.get(url, headers=headers)

    data = r.json()
    return data



def check_issue_exists(issue_number, board_name):
    query = "SELECT * from issues where issueNumber=%s AND boardName='%s'" %(issue_number, board_name)
    all_issues = db.with_query(query)
    return not all_issues

def fetch_issue_status(issue_number):
    zenhub_root_url = app.config['ZENHUB_ROOT_URL']
    issue_url = app.config['ZENHUB_ISSUE_URL']
    issue_url = issue_url.replace("{repositories_id}", app.config['REPOSITORIES_ID'])
    issue_url = issue_url.replace("{issue_number}", str(issue_number))

    headers = {'X-Authentication-Token': app.config['ZENHUB_AUTH_TOKEN']}
    url = zenhub_root_url + issue_url

    r = requests.get(url, headers=headers)

    data = r.json()
    if "is_epic" in data:
        if data["is_epic"] is False:
            if "pipeline" in data:
                return data["pipeline"]["name"]
            return "Closed"
    return "epic"

def get_issue(board_name, issue_number):
    query = "SELECT * from issues where issueNumber=%s AND boardName='%s' LIMIT 1" %(issue_number, board_name)
    issue = db.with_query(query)
    return loop_all_issues(issue)

def get_issues():
    all_issues = db.select_all_from_table("issues")
    return loop_all_issues(all_issues)

def loop_all_issues(all_issues):
    array_issues = {'issues':[]}
    for issue in all_issues:
        array_issues["issues"].append({
            "issueNumber": issue[0],
            "boardName": issue[1],
            "title": issue[2],
            "issueStatus": issue[3],
            "issueLink": issue[4]
        })

    return array_issues

def insert_issues(issue_number, board_name, title, issue_status, issue_link):
    query = "INSERT INTO issues (issueNumber, boardName, title, issueStatus, issueLink) VALUES (?, ?, ?, ?, ?)"
    args = (issue_number, board_name, title, issue_status, issue_link)
    return db.insert_query(query, args)

def delete_all_issues_for_board():
    delete_issues_query = "DELETE FROM issues where boardName = '%s'" %(app.config['REPOS'])
    db.with_query(delete_issues_query)
