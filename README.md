# SAIRAH

A bot to help setup FETI staging servers.

# Installation

```
git clone git@github.com:FluentEdge/sairah.git && cd sairah
```

```
heroku create your-app-name
```

```
heroku config:set SPECIAL_SECRET=whatever HEROKU_API_KEY=whatever HEROKU_BASE_APP_NAME=your-app
```

```
heroku ps:scale web=1
```

# Usage

Set these environment variables

```
# Required
SPECIAL_SECRET=secret-you-set-in-github-webhooks-configuration

# Set Heroku app name in environment so you can get full domain name within app
HEROKU_API_KEY=asdf1234-asdf1234-asdf1234
HEROKU_BASE_APP_NAME=your-app

# Set GitHub API keys

```

`HEROKU_BASE_APP_NAME` would be your original heroku app with review apps spawning from it.
