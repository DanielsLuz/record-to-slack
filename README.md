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

### Setup (for developers)
While it's not a distributed app, you have to do some configuration by yourself to properly reuse this code. 


The first step is the Slack's configuration:
* create a Slack app following [this guide](https://api.slack.com/slack-apps#creating_apps) 
* configure your redirect URLs
* add a BOT user that will be used to sending the recordings to your workspace

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

### Usage notes
The application's usage is pretty straight forward. Just login and add the app to your workspace, and you can start sending recordings to every channel the bot is invited to. 

**NOTE FOR WORKSPACE ADMINS**: the audio messages are posted by the bot user, which means that any channel the bot is in will appear in the select options, including **private** channels. If you have any channel that should NOT be exposed (even it's existence), do **NOT** invite the bot to it. No reading of messages is made by the bot, just the listing of channels it has access to.

**Reinforcing**: permissions are based on the bot's user, not on the logged in user, be careful with private channels exposure. Again, messages will not be read, but the channel's name will be seen and audio can be sent into that channel.

### TODO
* Setup app to be distributed via Slack (easier configuration for non developers)
* Add unit tests
* Refactor code to interact with Slack's API into it's own class
* Improve HTML/CSS (too much *display: flex*, maybe?)
* Add audio transcription (CTRL+F your audios!!!)

