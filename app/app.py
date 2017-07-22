from flask import Flask, render_template
from flask_assets import Environment, Bundle


app = Flask(__name__)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('css/main.scss', filters='pyscss', output='main.css')
assets.register('scss_all', scss)


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
    return render_template('index.pug')


if __name__ == '__main__':
    app.run()
