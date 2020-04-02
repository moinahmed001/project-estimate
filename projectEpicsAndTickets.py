import requests, json
import db
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def get_all_issues_from_project(board_name):
    query = "SELECT * from projectEpicsAndTickets where type ='issue' AND boardName='%s'" %(board_name)
    return db.with_query(query)
