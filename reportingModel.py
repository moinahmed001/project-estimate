import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_reporting():
    all_reporting = db.select_all_from_table("reporting")
    array_reporting = {'reporting':[]}
    for reporting in all_reporting:
        array_reporting["reporting"].append({
        "reportingId": reporting[0],
        "projectId": reporting[1],
        "contingencyId": reporting[2]
    })

    return array_reporting
