import requests, json
import db
import time
from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def fetch_epics(repoId):
    zenhub_root_url = app.config['ZENHUB_ROOT_URL']
    epics_url = app.config['EPICS_URL']
    epics_url = epics_url.replace("{repositories_id}", str(repoId))

    headers = {'X-Authentication-Token': app.config['ZENHUB_AUTH_TOKEN']}
    url = zenhub_root_url + epics_url

    print("Attempting to fetch epics, url is: %s" %(url))
    r = requests.get(url, headers=headers)
    print("Zenhub api rate used so far %s out 100" %(r.headers["X-RateLimit-Used"]))
    if int(r.headers["X-RateLimit-Used"]) > 95:
        sleep_for = (int(r.headers["X-RateLimit-Reset"]) - int(time.time())) + 1
        print("SLEEPING FOR %s seconds" %(sleep_for))
        time.sleep(sleep_for)
    data = r.json()
    return data

def get_epics():
    all_epics = db.select_all_from_table("epics")
    return loop_all_epics(all_epics)

def loop_all_epics(all_epics):
    array_epics = {'epics':[]}
    for epic in all_epics:
        array_epics["epics"].append({"epicId": epic[0], "epicName": epic[1]})

    return array_epics

def get_epic(epicId):
    query = "SELECT * from epics where epicId=%s LIMIT 1" %(epicId)
    all_epics = db.with_query(query)
    return loop_all_epics(all_epics)

def get_epic_by_board_name(board_name):
    query = "SELECT * from epics where boardName='%s'" %(board_name)
    all_epics = db.with_query(query)
    return loop_all_epics(all_epics)

def insert_epics(epic_issue_number, epic_title, board_name):
    query = "INSERT INTO epics (epicId, epicName, boardName) VALUES (?, ?, ?)"
    args = (epic_issue_number, epic_title, board_name)
    return db.insert_query(query, args)

def delete_all_epics_for_board(board_name):
    delete_epics_query = "DELETE FROM epics where boardName = '%s'" %(board_name)
    db.delete_query(delete_epics_query)
