from flask import Flask, escape, request, Blueprint, redirect, url_for, render_template
from views import views_routes
from ingestApi import ingest_api_routes
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, projectsModel, epicsIssuesModel, ticketsModel, userProjectAccessModel, reportingModel, epicsIssuesRemovedModel, contingencyModel, boardsModel
from flask import jsonify
from contextlib import closing
from requests.exceptions import RequestException
from requests import get
from deepdiff import DeepDiff
import json, re
from bs4 import BeautifulSoup


app = Flask(__name__)
app.register_blueprint(views_routes)
app.register_blueprint(ingest_api_routes)
app.config.from_pyfile('config.cfg')

@app.route('/')
def all_available_urls():
    routes = []
    for route in app.url_map.iter_rules():
        routes.append('{url: %s}' % route)
    return jsonify(routes)



@app.route('/api/post/project', methods=['GET', 'POST'])
def api_post_project():
    response = {}
    response["status"] = "error"
    if request.method == 'POST':
        # validate the form
        if projectsModel.validate_form(request.form):
            # check if the project already exists
            if projectsModel.get_project(request.form)["projects"] == []:

                # check if the board name is valid
                if boardsModel.get_board(request.form["repoId"])["boards"] != []:
                    projectsModel.insert_project(request.form)
                    project_id = projectsModel.get_project(request.form)["projects"][0]["projectId"]
                    url_created = 'views_routes.projectEpicsAndTickets'
                    response["redirectUrl"] = url_for(url_created, project_id=project_id)
                    response["status"] = "success"
                else:
                    response["message"] = "could not find the board "

            else:
                response["message"] = "This project already exists"

        else:
            response["message"] = "failed to validate the form"
            # response["projectData"] = request.form
            response["redirectUrl"] = url_for('views_routes.project')
    else:
        response["message"] = "request was not a POST "
        response["redirectUrl"] = url_for('views_routes.project')

    return jsonify(response)

@app.route('/api/post/projectEpicsAndTickets', methods=['GET', 'POST'])
def api_post_project_epics_and_tickets():
    response = {}
    response["status"] = "error"
    if request.method == 'POST':
        # validate the form
        if peatm.validate_form(request.form):
            # check if the projectEpicsAndTickets already has this epic in the db
            if peatm.get_epic_and_issue(request.form["projectId"], request.form["id"], request.form["type"])["projectEpicsAndTickets"] == []:
                type = request.form["type"]
                if type == 'epic':
                    peatm.insert_epic_and_issue(request.form)
                    url_created = 'views_routes.projectEpicsAndTickets'
                    response["redirectUrl"] = url_for(url_created, project_id=request.form["projectId"])
                    response["status"] = "success"
                # check if the type is issue and it belongs to an epic
                if type == 'issue':
                    if epicsIssuesModel.get_issue_epic(request.form["boardName"], request.form["id"])["epicsIssues"] == []:
                        peatm.insert_epic_and_issue(request.form)
                        url_created = 'views_routes.projectEpicsAndTickets'
                        response["redirectUrl"] = url_for(url_created, project_id=request.form["projectId"])
                        response["status"] = "success"
                    else:
                        response["message"] = "This issue belongs to an epic!"


            else:
                response["message"] = "This project epic/issue already exists"
        else:
            response["message"] = "failed to validate the form"
            # response["projectData"] = request.form
            response["redirectUrl"] = url_for('views_routes.project')
    else:
        response["message"] = "request was not a POST "
        response["redirectUrl"] = url_for('views_routes.project')

    return jsonify(response)



@app.route('/api/epics')
def api_epics():
    return jsonify(epicsModel.get_epics())

@app.route('/api/boards')
def api_boards():
    return jsonify(boardsModel.get_boards())

@app.route('/api/issues')
def api_issues():
    return jsonify(issuesModel.get_issues())

@app.route('/api/projectEpicsAndTickets')
def api_project_epics_and_tickets():
    return jsonify(peatm.get_epics_and_issues())

@app.route('/api/epicsIssues')
def api_epics_issues():
    return jsonify(epicsIssuesModel.get_epics_issues())

@app.route('/api/projects')
def api_projects():
    return jsonify(projectsModel.get_projects())

@app.route('/api/tickets')
def api_tickets():
    return jsonify(ticketsModel.get_tickets())

@app.route('/api/userProjectAccess')
def api_user_project_access():
    return jsonify(userProjectAccessModel.get_user_project_access())

@app.route('/api/reporting')
def api_reporting():
    return jsonify(reportingModel.get_reporting())

@app.route('/api/contingency')
def api_contingency():
    return jsonify(contingencyModel.get_contingency())

@app.route('/api/epicsIssuesRemoved')
def api_epics_issues_removed():
    return jsonify(epicsIssuesRemovedModel.get_epics_issues_removed())

@app.route('/api/issue/<board_name>/<issue_number>')
def api_issue(board_name, issue_number):
    return issuesModel.get_issue(board_name, issue_number)

@app.route('/api/post/ticket/<board_name>/<issue_number>', methods=['POST'])
def api_post_ticket(board_name, issue_number):
    if request.method == 'POST':
        issue_details = issuesModel.fetch_issue_from_github(board_name, issue_number)
        ticket_issue = {"boardName": board_name, "issueNumber": issue_number, "totalComments": issue_details["comments"],
        "dependantSystem": request.form["dependantSystem"],
        "dependantReason": request.form["dependantReason"],
        "devEstimateInDays": request.form["devEstimateInDays"],
        "qaEstimateInDays": request.form["qaEstimateInDays"],
        "proposedReleaseDropTo": request.form["proposedReleaseDropTo"],
        "notes": request.form["notes"],
        "sharedPlatformIssue": request.form["sharedPlatformIssue"]
        }
        ticketsModel.insert_or_update_ticket(ticket_issue)
        return redirect(url_for('views_routes.projectEpicsAndTickets', project_id=request.form["projectId"]))

# this fetches and inserts individual issue
# it will also insert/update ticket
@app.route('/api/github/issue/<board_name>/<issue_number>')
def api_github_issue(board_name, issue_number):
    issue_details = issuesModel.fetch_issue_from_github(board_name, issue_number)
    ticket_issue = {"boardName": board_name, "issueNumber": issue_number, "totalComments": issue_details["comments"]}
    ticketsModel.insert_or_update_ticket_comment_count(ticket_issue)

    if api_issue(board_name, issue_number)["issues"] == []:
        issue_does_not_exists = issuesModel.check_issue_exists(issue_number, board_name)
        if issue_does_not_exists:
            repoId = boardsModel.get_repo_id(board_name)
            issue_status = issuesModel.fetch_issue_status(issue_number, repoId)
            if issue_status is not "epic":
                issuesModel.insert_issues(issue_number, board_name, issue_details['title'], issue_status, issue_details["html_url"])

    return api_issue(board_name, issue_number)

@app.route('/api/epicsIssues/<board_name>/<epic_number>')
def api_epic_issues(board_name, epic_number):
    return epicsIssuesModel.get_epic_issues(board_name, epic_number)

@app.route('/api/epicIssuesFullDetails/<board_name>/<epic_number>')
def api_epic_issues_full_details(board_name, epic_number):
    return epicsIssuesModel.get_epic_issues_full_details(board_name, epic_number)


# config server
@app.route("/web/config/<territory>/<env>")
def web_config_check(territory, env):
    config_version_from = request.args.get('config_version_from', default = '4cf564f', type = str)
    config_version_to = request.args.get('config_version_to', default = 'aa1dfa9', type = str)
    if territory == 'es':
        if env == 'prod':
            full_url = 'https://www.sky.es/international/static/{0}/config/es/nowtv/nowtv/web/production/config.json'
        elif env == 'func':
            full_url = 'https://www.func.prod.sky.es/international/static/{0}/config/es/nowtv/nowtv/web/func-prod/config.json'
    elif territory == 'gb':
        if env == 'prod':
            full_url = 'https://www.nowtv.com/international/static/{0}/config/gb/nowtv/nowtv/web/production/config.json'
        elif env == 'func':
            full_url = 'https://www.func.prod.nowtv.com/international/static/{0}/config/gb/nowtv/nowtv/web/func-prod/config.json'
    elif territory == 'ie':
        if env == 'prod':
            full_url = 'https://www.nowtv.com/international/static/{0}/config/ie/nowtv/nowtv/web/production/config.json'
        elif env == 'func':
            full_url = 'https://www.func.prod.nowtv.com/international/static/{0}/config/ie/nowtv/nowtv/web/func-prod/config.json'
    elif territory == 'it':
        if env == 'prod':
            full_url = 'https://www.nowtv.it/international/static/{0}/config/it/nowtv/nowtv/web/production/config.json'
        elif env == 'func':
            full_url = 'https://c3.nowtv.it/international/static/{0}/config/it/nowtv/nowtv/web/func-prod/config.json'
    elif territory == 'de':
        if env == 'prod':
            full_url = 'https://skyticket.sky.de/international/static/{0}/config/de/nowtv/nowtv/web/production/config.json'
        elif env == 'func':
            full_url = 'https://test.skyticket.sky.de/international/static/{0}/config/de/nowtv/nowtv/web/func-prod/config.json'



    url = full_url.format(config_version_from)
    url_to_compare = full_url.format(config_version_to)

    old_url_fetched_response = simple_get_json(url).decode('utf-8')
    new_url_fetched_response = simple_get_json(url_to_compare).decode('utf-8')

    diff_result = DeepDiff(json.loads(old_url_fetched_response), json.loads(new_url_fetched_response), ignore_order=True)

    try:
        return render_template("config_diff_web.html", live_config_hash = all_config_hash(env), diff_result = diff_result, territory=territory, config_version_from=config_version_from, config_version_to=config_version_to, env=env, url=url, url_to_compare=url_to_compare)
    except Exception as e:
        return str(e)

@app.route("/web/config/<env>/hash")
def web_config_hash(env):
    return jsonify(all_config_hash(env))


def all_config_hash(env):
    live_config_hash = {}
    if env == 'prod':
        all_urls = [
            "https://www.nowtv.com/gb/watch/home", "https://www.nowtv.com/ie/watch/home", "https://skyticket.sky.de/watch/home", "https://www.nowtv.it/watch/home", "https://www.sky.es/ver/inicio"
        ]
    else:
        all_urls = [
            "https://www.func.prod.nowtv.com/gb/watch/home", "https://test.skyticket.sky.de/watch/home", "https://c3.nowtv.it/watch/home", "https://www.func.prod.sky.es/ver/inicio"
        ]
        # "https://func.prod.nowtv.com/ie/watch/home",

    for url in all_urls:
        if url == "https://test.skyticket.sky.de/watch/home":
            raw_html = simple_get(url, auth=('StormSkyDE', '1Jky73spyy!'))
        elif url == "https://c3.nowtv.it/watch/home":
            raw_html = simple_get(url, auth=('river', 'PWD!sky0nl1n3#2014'))
        else:
            raw_html = simple_get(url)

        if raw_html != None:
            html = BeautifulSoup(raw_html, 'html.parser')
            string_html = raw_html.decode("utf-8").split()
            release_hash = 'UNKNOWN'


            for aString in string_html:
                if "href" in aString:
                    hash = re.findall(r'static\/(.*?)\/core', aString)
                    if len(hash) == 1:
                        release_hash = hash[0]
                        live_config_hash[url] = hash[0]
                        break

    return live_config_hash


def simple_get_json(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def simple_get(url, auth=()):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, auth=auth)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None)
