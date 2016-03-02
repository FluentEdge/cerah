# SAIRAH

A bot to help setup FETI staging servers.

# Installation

Clone, deploy to heroku, set env vars!

# Usage

Set these environment variables

```
HEROKU_API_KEY=asdf1234-asdf1234-asdf1234
HEROKU_BASE_APP_NAME=some-app
```

`HEROKU_BASE_APP_NAME` would be your original heroku app with review apps spawning from it.

# Testing

`pip install -r requirements.dev.txt`
`py.test`
