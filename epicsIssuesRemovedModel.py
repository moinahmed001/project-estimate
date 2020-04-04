import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_epics_issues_removed():
    all_epics_issues_removed = db.select_all_from_table("epicsIssuesRemoved")
    array_epics_issues_removed = {'epicsIssuesRemoved':[]}
    for epicsIssuesRemoved in all_epics_issues_removed:
        array_epics_issues_removed["epicsIssuesRemoved"].append({
        "epicsIssuesRemovedId": epicsIssuesRemoved[0],
        "epicId": epicsIssuesRemoved[1],
        "issueNumber": epicsIssuesRemoved[2]
    })

    return array_epics_issues_removed
