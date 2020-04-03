import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_projects():
    all_projects = db.select_all_from_table("projects")
    array_projects = {'projects':[]}
    for project in all_projects:
        array_projects["projects"].append({
            "projectId": project[0],
            "userId": project[1],
            "projectName": project[2],
            "businesReqUrl": project[3],
            "projectManager": project[4],
            "architect": project[5],
            "productOwner": project[6],
            "trialDate": project[7],
            "releaseDate": project[8]
        })

    return array_projects
