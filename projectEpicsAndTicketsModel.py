import requests, json
import db
import ticketsModel, epicsIssuesModel, epicsModel
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

def get_all_issues_from_project(board_name):
    query = "SELECT peat.projectEpicsAndTicketsId, peat.projectId, peat.id, peat.type from projectEpicsAndTickets as peat JOIN projects as p ON p.projectId = peat.projectId WHERE p.boardName='%s'" %(board_name)
    return db.with_query(query)

def get_epics_and_issues():
    all = db.select_all_from_table("projectEpicsAndTickets")
    return loop_all_issues(all)

def get_epic_and_issue(projectId, id, type):
    query = "SELECT * from projectEpicsAndTickets where projectId=%s AND id=%s AND type='%s' LIMIT 1" %(projectId, id, type)
    project = db.with_query(query)
    return loop_all_issues(project)

def get_epics_and_issues_with_project_id(projectId):
    query = "SELECT peat.id, peat.type, peat.projectId, p.boardName from projectEpicsAndTickets as peat JOIN projects as p ON p.projectId = peat.projectId where peat.projectId=%s" %(projectId)
    project_epics_and_issues = db.with_query(query)

    array_issues = {'projectEpicsIssues':[]}
    for epic_and_issue in project_epics_and_issues:
        if epic_and_issue is not None:
            boardName = epic_and_issue[3]

            if epic_and_issue[1] == 'epic':
                epic_number = epic_and_issue[0]
                if epicsModel.get_epic(epic_number)["epics"] != []:
                    all_epics_issues = epicsIssuesModel.get_epic_issues(boardName, epic_number)["epicsIssues"]
                    epic_name = epicsModel.get_epic(epic_number)["epics"][0]["epicName"]
                    array_issues["projectEpicsIssues"].append({"epicName": epic_name, "allTickets": []})

                    for epic_issue in all_epics_issues:
                        if epic_issue is not None:
                            ticket = ticketsModel.get_tickets_with_boardName_and_issueNumber(boardName, epic_issue["issueNumber"])
                            print(">>>>>")
                            print(epic_issue)
                            print(">>>>> adding ticket: ")

                            print(ticket)
                            array_issues["projectEpicsIssues"][-1]["allTickets"].append(ticket)

            elif epic_and_issue[1] == 'issue':
                print(">>>>> issue type: SHouldnt be here!")
                print(epic_and_issue)
                # TODO: test this path!
                issueNumber = epic_and_issue[0]
                ticket = ticketsModel.get_tickets_with_boardName_and_issueNumber(boardName, issueNumber)
                # array_issues["projectEpicsIssues"].append(ticket)
    return array_issues

def get_all_epics_issues_for_project(projectId):
    query = "SELECT peat.projectId, ei.epicId, ei.boardName, i.issueNumber, i.title, i.issueStatus, i.issueLink from projectEpicsAndTickets as peat JOIN epicsIssues ei ON peat.id=ei.epicId JOIN issues i ON ei.issueNumber=i.issueNumber where peat.projectId=%s AND peat.type='epic'" %(projectId)
    all_epic_ids = db.with_query(query)

    array_issues = {'projectEpicsIssues':[]}
    for issue in all_epic_ids:
        array_issues["projectEpicsIssues"].append({
            "projectId": issue[0],
            "epicId": issue[1],
            "boardName": issue[2],
            "issueNumber": issue[3],
            "title": issue[4],
            "issueStatus": issue[5],
            "issueLink": issue[6]
        })
    return array_issues

def get_all_individual_issues_for_project(projectId):
    return True


def loop_all_issues(all):
    array_issues = {'projectEpicsAndTickets':[]}
    for issue in all:
        array_issues["projectEpicsAndTickets"].append({
            "projectEpicsAndTicketsId": issue[0],
            "projectId": issue[1],
            "id": issue[2],
            "type": issue[3]
        })

    return array_issues

def validate_form(form):
    if all (k in form for k in ("projectId", "id", "type")):
        return True
    return False

def insert_epic_and_issue(form):
    query = "INSERT INTO projectEpicsAndTickets (projectId, id, type) VALUES (?, ?, ?)"

    args = (check_field_and_get_value(form, "projectId"), check_field_and_get_value(form, "id"), check_field_and_get_value(form, "type"))
    return db.insert_query(query, args)


def check_field_and_get_value(form, field):
    if field in form:
        return form[field]
    else:
        return None
