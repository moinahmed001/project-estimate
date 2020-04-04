import requests, json
import db
from flask import Flask

app = Flask(__name__)


def get_boards():
    all_boards = db.select_all_from_table("boards")
    return loop_all_boards(all_boards)

def get_board(repo_id):
    query = "SELECT * from boards where repoId=%s LIMIT 1" %(repo_id)
    board = db.with_query(query)
    return loop_all_boards(board)

def loop_all_boards(all_boards):
    array_board = {'boards':[]}
    for board in all_boards:
        array_board["boards"].append({
        "repoId": board[0],
        "boardName": board[1]
    })
    return array_board
