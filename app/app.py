import os
import requests
import json
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


@app.route('/', methods=['GET', 'POST'])
def index():
    token = session.get('access_token', None)
    channels = []
    if token is not None:
        slack = Slacker(token)

        if request.method == 'POST':
            tofilter = json.loads(request.form['filtchannels'])
            for ch in tofilter['tofilter']:
                slack.channels.archive(ch['id'])

        channels_response = slack.channels.list(exclude_archived=True)
        channels = channels_response.body['channels']
        for i, channel in enumerate(channels):
            channel_details_resp = slack.channels.info(channel['id'])
            channel_details = channel_details_resp.body['channel']
            if 'latest' in channel_details:
                channels[i]['last_event'] = channel_details['latest']['ts']
            else:
                channels[i]['last_event'] = '-1'

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
