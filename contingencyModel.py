import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_contingency():
    all_contingency = db.select_all_from_table("contingency")
    array_contingency = {'contingency':[]}
    for contingency in all_contingency:
        array_contingency["contingency"].append({
        "contingencyId": contingency[0],
        "title": contingency[1],
        "percentage": contingency[2],
        "description": contingency[3]
    })

    return array_contingency
