import os
import requests
from flask import Flask, render_template, request, redirect, session
from flask_assets import Environment, Bundle
from slacker import Slacker


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('assets/main.scss', filters='pyscss', output='css/main.css')
assets.register('scss_all', scss)

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']


def findby_num_members(num):
    channels_response = slack.channels.list(1)
    channels = channels_response.body['channels']
    channels_to_archive = []
    for channel in channels:
        if channel['num_members'] <= num:
            channels_to_archive.append(channel)
    print channels_to_archive


def findby_latest(date):
    channels_response = slack.channels.list(1)
    channels = channels_response.body['channels']
    channels_to_archive = []
    date = date_to_ts(date)
    print date
    for channel in channels:
        channel_details_response = slack.channels.info(channel['id'])
        channel_details = channel_details_response.body['channel']
        latest_message_ts = channel_details['latest']['ts']
        print latest_message_ts
        if latest_message_ts < date:
            channels_to_archive.append(channel)
    print channels_to_archive


@app.route('/', methods=['GET', 'POST'])
def index():
    token = session.get('access_token', None)
    channels = []
    if token is not None:
        slack = Slacker(token)
        channels_response = slack.channels.list(exclude_archived=True)
        channels = channels_response.body['channels']
        for i, channel in enumerate(channels):
            channel_details_resp = slack.channels.info(channel['id'])
            channel_details = channel_details_resp.body['channel']
            if 'latest' in channel_details:
                channels[i]['last_event'] = channel_details['latest']['ts']
            else:
                channels[i]['last_event'] = '-1'

        print(channels)
    return render_template('index.pug', channels=channels)


@app.route('/oauth')
def oauth():
    if 'error' in request.args:
        return redirect('/')

    code = request.args.get('code')

    token_url = 'https://slack.com/api/oauth.access'
    token_url_data = {'client_id': client_id, 'client_secret': client_secret,
                      'code': code}
    resp = requests.get(token_url, params=token_url_data)
    jsoned = resp.json()
    session['access_token'] = jsoned['access_token']
    return redirect('/')


if __name__ == '__main__':
    app.run()
