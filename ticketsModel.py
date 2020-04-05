import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_tickets():
    all_tickets = db.select_all_from_table("tickets")
    return loop_all_tickets(all_tickets)

def get_tickets_with_boardName_and_issueNumber(boardName, issueNumber):
    query = "SELECT * from tickets where issueNumber=%s AND boardName='%s' LIMIT 1" %(issueNumber, boardName)
    all_tickets = db.with_query(query)
    return loop_all_tickets(all_tickets)

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
