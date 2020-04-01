import requests, json
import db
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def fetch_issue(issue_number):
    github_root_url = app.config['GITHUB_ROOT_URL']
    issue_url = app.config['ISSUE_URL']
    issue_url = issue_url.replace("{repos}", app.config['REPOS'])
    issue_url = issue_url.replace("{issue_number}", str(issue_number))

    headers = {'Accept': app.config['GITHUB_ACCEPT_HEADER'], 'Authorization': app.config['GITHUB_AUTH_TOKEN']}
    url = github_root_url + issue_url

    r = requests.get(url, headers=headers)

    data = r.json()
    return data

def get_issue(issue_number):
    all_issues = db.select_all_from_table("issues")
    array_issues = {'issues':[]}
    for issue in all_issues:
        array_issues["issues"].append({"issueNumber": issue[0], "boardName": issue[1], "title": issue[2], "issueStatus": issue[3], "issueLink": issue[4]})

    return array_issues
