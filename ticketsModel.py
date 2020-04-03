import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_tickets():
    all_tickets = db.select_all_from_table("tickets")
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
