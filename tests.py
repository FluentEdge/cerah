import hmac
import json
import mock
import os

from bottle import debug
from hashlib import sha1
from unittest import TestCase
from webtest import TestApp

from server import app, env


app = TestApp(app)
debug(True)

SECRET = os.environ.get("SPECIAL_SECRET")


class SairahTests(TestCase):

    @staticmethod
    def github_webhook_response(endpoint, extra_payload=None, **kwargs):
        payload = {
            "pull_request": {
                "number": 1
            }
        }
        body = json.dumps(payload)
        if extra_payload:
            payload.update(extra_payload)
        if 'headers' not in kwargs:
            signature = hmac.new(SECRET, body, sha1).hexdigest()
            kwargs['headers'] = {'X-Hub-Signature': "sha={}".format(signature)}
        if 'content_type' not in kwargs:
            kwargs['content_type'] = "application/json"
        return app.post(endpoint, body, **kwargs)

    def test_index_returns_nice_message(self):
        resp = app.get('/')
        assert resp.body == "Hello, I am <a href='https://github.com/FluentEdge/SAIRAH'>SAIRAH</a> " \
                            "a bot to help with deployments!"

    def test_verifies_github_signature(self):
        with mock.patch('server.set_heroku_config') as set_heroku_config_mock:
            resp = self.github_webhook_response(
                "/pr_created",
                headers={'X-Hub-Signature': "sha=asdf"},
                expect_errors=True
            )
            assert resp.status_code == 403

    def test_set_heroku_app_name_only_when_env_var_set(self):
        del env['HEROKU_BASE_APP_NAME']
        with mock.patch('server.set_heroku_config') as set_heroku_config_mock:
            self.github_webhook_response("/pr_created")
        assert not set_heroku_config_mock.called

        env['HEROKU_BASE_APP_NAME'] = 'test'
        with mock.patch('server.set_heroku_config') as set_heroku_config_mock:
            self.github_webhook_response("/pr_created")
        assert set_heroku_config_mock.called
