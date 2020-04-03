# project-estimate
To install you will need to make sure you have the following
```
$ -> pip3 --version
pip 19.0.3 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
```

```
$ -> python3 --version
Python 3.7.3
```

## To install the application
```$ -> pip install -r requirements.txt```

## Pre-requisition
`You will need to get Zenhub and Github oauth token`

Zenhub API along with the link to fetch token: https://github.com/ZenHubIO/API#authentication
Github API requires you to go to `Settings` -> `Developer Settings` -> `Personal access tokens` or this link: https://github.com/settings/tokens

Once you have generated the token, you will need to `Enable SSO` from the Personal access token page above.

Once you have both tokens open `config.cfg` and update `ZENHUB_AUTH_TOKEN` and `GITHUB_AUTH_TOKEN`(do not delete the word token)

## To run the application
```$ -> env FLASK_APP=app.py flask run```

To enable the app in debug mode such that you do not have to stop start for each changes, run this on the terminal:
`export FLASK_DEBUG=1`


## To do tasks
There are some tasks in the `todo.txt` file should you want to get involved. Please add more ideas/issues as you develop
