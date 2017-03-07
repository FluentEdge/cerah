# SAIRAH

A bot to help setup staging servers for Heroku's [Review Apps](https://devcenter.heroku.com/articles/github-integration-review-apps). Particularly useful for keep secret keys out of version control.

* You define some env vars on SAIRAH
* Add web hooks to GitHub pointing at SAIARAH
* SAIRAH server listens for new PRs, then when the Review app server is built the ENV vars are set.

# Installation

### Setup the Heroku server
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

### Add web hook

![image](https://cloud.githubusercontent.com/assets/2185159/23642266/2607ea08-02ae-11e7-95f2-3a54303133f4.png)

Under `Let me select individual events.` check `Pull Request`

![image](https://cloud.githubusercontent.com/assets/2185159/23642284/4bc5f280-02ae-11e7-8ffb-586be709d875.png)

Now when new servers are created, SAIRAH sets their env vars! Or whatever else you need to do.

# Usage

Set these environment variables

```
# Required
SPECIAL_SECRET=secret-you-set-in-github-webhooks-configuration

# Set Heroku app name in environment so you can get full domain name within app
HEROKU_API_KEY=asdf1234-asdf1234-asdf1234
HEROKU_BASE_APP_NAME=your-app
```

`HEROKU_BASE_APP_NAME` would be your original heroku app with review apps spawning from it.
