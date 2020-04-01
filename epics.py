import requests, json
import db
from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def fetch_epics():
    zenhub_root_url = app.config['ZENHUB_ROOT_URL']
    epics_url = app.config['EPICS_URL']
    epics_url = epics_url.replace("{repositories_id}", app.config['REPOSITORIES_ID'])

    headers = {'X-Authentication-Token': app.config['ZENHUB_AUTH_TOKEN']}
    url = zenhub_root_url + epics_url

    r = requests.get(url, headers=headers)

    data = r.json()
    return data

def get_epics():
    all_epics = db.select_all_from_table("epics")
    array_epics = {'epics':[]}
    for epic in all_epics:
        array_epics["epics"].append({"epic_id": epic[0], "epicName": epic[1]})

    return array_epics
