import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_tickets():
    all_tickets = db.select_all_from_table("tickets")
    return loop_all_tickets(all_tickets)

def get_tickets_with_boardName_and_issueNumber(boardName, issueNumber):
    query = "SELECT t.issueNumber, i.issueLink, i.title, t.dependantSystem, t.dependantReason, t.devEstimateInDays, t.qaEstimateInDays, i.issueStatus, t.proposedReleaseDropTo, t.totalComments, t.notes, t.sharedPlatformIssue, t.ticketId from tickets as t JOIN issues as i on t.issueNumber=i.issueNumber AND t.boardName=i.boardName where t.issueNumber=%s AND t.boardName='%s' LIMIT 1" %(issueNumber, boardName)
    ticket = db.with_query(query)
    array_ticket = {}
    if ticket != []:
        array_ticket = {
            "issueNumber": ticket[0][0],
            "issueLink": ticket[0][1],
            "title": ticket[0][2],
            "dependantSystem": ticket[0][3],
            "dependantReason": ticket[0][4],
            "devEstimateInDays": ticket[0][5],
            "qaEstimateInDays": ticket[0][6],
            "issueStatus": ticket[0][7],
            "proposedReleaseDropTo": ticket[0][8],
            "totalComments": ticket[0][9],
            "notes": ticket[0][10],
            "sharedPlatformIssue": ticket[0][11],
            "ticketId": ticket[0][12]
        }

    return array_ticket

def loop_all_tickets(all_tickets):
    array_tickets = {'tickets':[]}
    for ticket in all_tickets:
        array_tickets["tickets"].append({
            "ticketId": ticket[0],
            "boardName": ticket[1],
            "issueNumber": ticket[2],
            "dependantSystem": ticket[3],
            "dependantReason": ticket[4],
            "devEstimateInDays": ticket[5],
            "qaEstimateInDays": ticket[6],
            "proposedReleaseDropTo": ticket[7],
            "totalComments": ticket[8],
            "notes": ticket[9],
            "sharedPlatformIssue": ticket[10]
        })

    return array_tickets

def insert_or_update_ticket(data):

    if all (k in data for k in ("boardName", "issueNumber")):
        query = "SELECT totalComments from tickets where issueNumber=%s AND boardName='%s' LIMIT 1" %(data["issueNumber"], data["boardName"])
        ticket = db.with_query(query)
        if ticket != []:
            # update the table
            q = "UPDATE tickets SET dependantSystem=?, dependantReason=?, devEstimateInDays=?, qaEstimateInDays=?, proposedReleaseDropTo=?, totalComments=?, notes=?, sharedPlatformIssue=? WHERE issueNumber=? AND boardName=?"
            args = (check_field_and_get_value(data, "dependantSystem"), check_field_and_get_value(data, "dependantReason"), check_field_and_get_value(data, "devEstimateInDays"), check_field_and_get_value(data, "qaEstimateInDays"), check_field_and_get_value(data, "proposedReleaseDropTo"), check_field_and_get_value(data, "totalComments"), check_field_and_get_value(data, "notes"), check_field_and_get_value(data, "sharedPlatformIssue"), data["issueNumber"], data["boardName"])

            db.insert_query(q, args)
        else:
            # add it to the db
            query = "INSERT INTO tickets (boardName, issueNumber, dependantSystem, dependantReason, devEstimateInDays, qaEstimateInDays, proposedReleaseDropTo, totalComments, notes, sharedPlatformIssue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = (check_field_and_get_value(data, "boardName"), check_field_and_get_value(data, "issueNumber"), check_field_and_get_value(data, "dependantSystem"), check_field_and_get_value(data, "dependantReason"), check_field_and_get_value(data, "devEstimateInDays"), check_field_and_get_value(data, "qaEstimateInDays"), check_field_and_get_value(data, "proposedReleaseDropTo"), check_field_and_get_value(data, "totalComments"), check_field_and_get_value(data, "notes"), check_field_and_get_value(data, "sharedPlatformIssue"))
            return db.insert_query(query, args)

    return "Error: Need the boardName and issueNumber to proceed"

def insert_or_update_ticket_comment_count(data):
    if all (k in data for k in ("boardName", "issueNumber")):
        query = "SELECT totalComments from tickets where issueNumber=%s AND boardName='%s' LIMIT 1" %(data["issueNumber"], data["boardName"])
        ticket = db.with_query(query)

        if ticket != [] and "totalComments" in data:
            if data["totalComments"] != ticket[0][0]:
                # update the table
                q = "UPDATE tickets SET totalComments = %s WHERE issueNumber=%s AND boardName='%s'" %(data["totalComments"], data["issueNumber"], data["boardName"])
                db.update_query(q)
        else:
            # add it to the db
            query = "INSERT INTO tickets (boardName, issueNumber, dependantSystem, dependantReason, devEstimateInDays, qaEstimateInDays, proposedReleaseDropTo, totalComments, notes, sharedPlatformIssue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = (check_field_and_get_value(data, "boardName"), check_field_and_get_value(data, "issueNumber"), check_field_and_get_value(data, "dependantSystem"), check_field_and_get_value(data, "dependantReason"), check_field_and_get_value(data, "devEstimateInDays"), check_field_and_get_value(data, "qaEstimateInDays"), check_field_and_get_value(data, "proposedReleaseDropTo"), check_field_and_get_value(data, "totalComments"), check_field_and_get_value(data, "notes"), check_field_and_get_value(data, "sharedPlatformIssue"))
            return db.insert_query(query, args)

    return "Error: Need the boardName and issueNumber to proceed"


def check_field_and_get_value(data, field):
    if field in data:
        return data[field]
    else:
        return None
