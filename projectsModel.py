import requests, json
import db, boardsModel
from flask import Flask

app = Flask(__name__)


def get_projects():
    all_projects = db.select_all_from_table("projects")
    return loop_all_projects(all_projects)

def get_project(form):
    if all (k in form for k in ("projectCreateduserId", "projectName", "repoId")):

        query = "SELECT * from projects where projectCreateduserId=%s AND projectName='%s' AND boardName='%s' LIMIT 1" %(check_field_and_get_value(form, "projectCreateduserId"), check_field_and_get_value(form, "projectName"), fetch_board_name(form))
        project = db.with_query(query)
        return loop_all_projects(project)

    return {'projects':[]}

def get_project_with_id(projectId):
    query = "SELECT * from projects where projectId=%s LIMIT 1" %(projectId)
    project = db.with_query(query)
    return loop_all_projects(project)

def fetch_board_name(form):
    repo_id = check_field_and_get_value(form, "repoId")
    board_name = None
    if repo_id is not None:
        if boardsModel.get_board(repo_id)["boards"] != []:
            board_name = boardsModel.get_board(repo_id)["boards"][0]["boardName"]
    return board_name

def validate_form(form):
    if all (k in form for k in ("projectCreateduserId", "projectName", "repoId")):
        return True
    return False

def insert_project(form):
    query = "INSERT INTO projects (projectCreateduserId, projectName, boardName, businessReqUrl, projectManager, architect, productOwner, trialDate, releaseDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    args = (check_field_and_get_value(form, "projectCreateduserId"), check_field_and_get_value(form, "projectName"), fetch_board_name(form), check_field_and_get_value(form, "businessReqUrl"), check_field_and_get_value(form, "projectManager"), check_field_and_get_value(form, "architect"), check_field_and_get_value(form, "productOwner"), check_field_and_get_value(form, "trialDate"), check_field_and_get_value(form, "releaseDate"))

    return db.insert_query(query, args)


def check_field_and_get_value(form, field):
    if field in form:
        return form[field]
    else:
        return None

def loop_all_projects(all_projects):
    array_projects = {'projects':[]}
    for project in all_projects:
        array_projects["projects"].append({
            "projectId": project[0],
            "projectCreateduserId": project[1],
            "projectName": project[2],
            "boardName": project[3],
            "businessReqUrl": project[4],
            "projectManager": project[5],
            "architect": project[6],
            "productOwner": project[7],
            "trialDate": project[8],
            "releaseDate": project[9]
        })
    return array_projects
