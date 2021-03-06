# record-to-slack
> A simple way to send audio recordings to Slack

**Disclaimer**: This application is developed mainly as a learning experience.

It is not the most beautiful page you ever see, I know... But it fulfills it's purpose, which is:

* For the user:
  * Record and send audio to some Slack channel as simple as possible
* For me:
  * Get some experience using Python (and Flask)
  * Learn how to integrate a bot with Slack's API
  * Make something somewhat useful (disagreeable, I know)

### Demo
The app is hosted on heroku, you can check it at: https://record-to-slack.herokuapp.com/login

### Usage notes
The application's usage is pretty straight forward. Just login and add the app to your workspace, and you can start sending recordings to every channel the bot is invited to.

### Setup (for developers)
The app is now distributed, which means you can add it directly to other workspaces.
If you want to checkout the code and host it yourself, you need to do some setup before.

The first step is the Slack's configuration:
* create a Slack app following [this guide](https://api.slack.com/slack-apps#creating_apps)
* configure your redirect URLs

Second step is to configure your hosting.
* Some environment variables are required
  * **APP_SECRET_KEY**: Flask's app secret key. See: [Flask's documentation](http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
  * **SLACK_CLIENT_ID**: From your created app on first step.
  * **SLACK_CLIENT_SECRET**: From your created app on first step.
  * **SLACK_APP_ID**: From your created app on first step.
  * **SLACK_REDIRECT_URI**: URI on your app used to redirect Slack's OAuth login. See: [Sign in with Slack](https://api.slack.com/docs/sign-in-with-slack).
  * **SLACK_REDIRECT_ADD_URI**: URI on your app used to redirect Slack's OAuth "Add to Slack" button. See: [Slack button](https://api.slack.com/docs/slack-button).
  * **DATABASE_URL**: Well... Your database URL.

Database migrations are done using [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/), remember to **init your database**!

**Note**: I hosted it on [Heroku](https://www.heroku.com/) (there are some parts of the code attached to it) modify it to fit your needs at your will.

You should be good to go! Just access the app, login and add it to your workspace.

### TODO
* ~~Setup app to be distributed via Slack (easier configuration for non developers)~~
* Add unit tests
* Refactor code to interact with Slack's API into it's own class
* Improve HTML/CSS (too much *display: flex*, maybe?)
* Add audio transcription (CTRL+F your audios!!!)

