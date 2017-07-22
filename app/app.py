from flask import Flask, render_template
from flask_assets import Environment, Bundle


app = Flask(__name__)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', filters='pyscss', output='main.css')
assets.register('scss_all', scss)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.pug')
