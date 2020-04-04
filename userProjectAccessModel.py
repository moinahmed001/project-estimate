import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_user_project_access():
    all_accesses = db.select_all_from_table("userProjectAccess")
    array_accesses = {'userProjectAccess':[]}
    for access in all_accesses:
        array_accesses["userProjectAccess"].append({
        "accessId": access[0],
        "userId": access[1],
        "proejctId": access[2]
    })

    return array_accesses
