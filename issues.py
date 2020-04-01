
# curl -X GET -H 'Accept: application/vnd.github.inertia-preview+json' -H 'Authorization: token d9cfcd75e27e7c0e7ea3de07fc1c7f0a83b9fd43' https://api.github.com/repos/sky-uk/ott-web-europe/issues/143
import requests, json
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
