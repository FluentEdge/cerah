import heroku3
import hmac
import logging
import os
import time

from bottle import Bottle, get, run, post, request, HTTPError
from hashlib import sha1


app = Bottle()


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
required_env_var_names = (
    'SPECIAL_SECRET',
)
optional_env_var_names = (
    'HEROKU_API_KEY',
    'HEROKU_BASE_APP_NAME',
)
env = {}
for name in required_env_var_names + optional_env_var_names:
    env[name] = os.environ.get(name, None)
    if env[name] in required_env_var_names:
        assert env[name], "Missing environment variable: %s" % name


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def set_heroku_config(application_name, key, value):
    conn = heroku3.from_key(env['HEROKU_API_KEY'])

    # Try at most 5 times to do this
    for _ in range(5):
        if conn.apps().get(application_name):
            app = conn.apps()[application_name]
            app.config()[key] = value  # this actually saves itself when you set it!
            return True
        time.sleep(5)
    return False


# ----------------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------------
@app.post('/pr_created')
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

    what_i_done = []

    if 'HEROKU_BASE_APP_NAME' in env:
        pr_number = request.json["pull_request"]["number"]
        new_app_name = "{}-pr-{}".format(env['HEROKU_BASE_APP_NAME'], pr_number)
        result = set_heroku_config(new_app_name, "HEROKU_APP_NAME", new_app_name)
        if not result:
            return "Could not find {} heroku app to set config stuff up...".format(new_app_name)
        what_i_done.append("Setup Heroku base app name")

    # Format what we did so tabs in front, newline on end
    what_i_done = ["\t{}\n".format(s) for s in what_i_done]
    return "OK, here's what I did: \n{}".format(''.join(what_i_done))


@app.get("/")
def nice_index():
    return "Hello, I am <a href='https://github.com/FluentEdge/SAIRAH'>SAIRAH</a> a bot to help with deployments!"


# ----------------------------------------------------------------------------
# Server
# ----------------------------------------------------------------------------
# Heroku sets PORT env var
if __name__ == '__main__':
    run(app=app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
