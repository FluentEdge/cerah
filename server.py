import json
import heroku3
import hmac
import logging
import os

from bottle import get, run, post, request, HTTPError
from hashlib import sha1


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
env_var_names = (
    'HEROKU_API_KEY',
    'HEROKU_BASE_APP_NAME'
    'SPECIAL_SECRET',
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
    # We need to verify the message we received against our secret
    payload = request.body.read()
    # Example received signature: "sha1=51fb5125e4e65aa893911c89de283576d9c821b5"
    received_sig = request.headers['X-Hub-Signature'].split('=', 1)[1]
    computed_sig = hmac.new(env["SPECIAL_SECRET"], payload, sha1).hexdigest()
    if received_sig != computed_sig:
        logging.error('Received signature %r does not match' % received_sig)
        raise HTTPError(403, 'Signature mismatch')

    # The message has been verified, so let's process it!
    pr_number = request.json["pull_request"]["number"]
    new_app_name = "{}-pr-{}".format(env['HEROKU_BASE_APP_NAME'], pr_number)
    set_heroku_config(new_app_name, "HEROKU_APP_NAME", new_app_name)
    return "OK"


@get("/")
def nice_index():
    return "Hello, I am <a href='https://github.com/FluentEdge/SAIRAH'>SAIRAH</a> a bot to help with deployments!"


# ----------------------------------------------------------------------------
# Server
# ----------------------------------------------------------------------------
# Heroku sets PORT env var
if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))