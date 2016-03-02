import json
import heroku3
import os

from bottle import get, run, post, request, HTTPError, response
from requests import Session
from requests import post as request_post


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
env_var_names = (
    'HEROKU_API_KEY',
    #'SPECIAL_SECRET',
)
env = {}
for name in env_var_names:
    env[name] = os.environ.get(name, None)
    assert env[name], "Missing environment variable: %s" % name


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def set_heroku_config(application_name, key, value):
    conn = heroku3.from_key(env['HEROKU_API_KEY'])
    app = conn.apps()[application_name]
    app.config()[key] = value  # this actually saves itself when you set it!


# ----------------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------------
@post('/pr_created')
def pr_created():
    print request.json
    return "asdf"


@get("/")
def nice_index():
    return "Hello, I am <a href='https://github.com/FluentEdge/SAIRAH'>SAIRAH</a> a bot to help with deployments!"


# ----------------------------------------------------------------------------
# Server
# ----------------------------------------------------------------------------
# Heroku sets PORT env var
if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))