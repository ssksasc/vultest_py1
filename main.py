from datetime import timedelta
from flask import Flask, session, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
# from flask_wtf.csrf import CSRFProtect

from dbcon import db
import page.index
import util

app = Flask(__name__, static_folder='resources', static_url_path='/resources')
app.config['SECRET_KEY'] = b'\x95[\xd5%"P\xeakP\xed\xd1\x14\xef\xd3\xddWCD\xfe\xcf(T\xd0\xb0'
# csrf = CSRFProtect(app)

app.jinja_env.filters['dateformat'] = util.strfdate


@app.before_request
def before_request():
    if not request.path.startswith('/resources/'):
        db.connect()
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=2)
        session.modified = True

@app.after_request
def after_request(response):
    if not request.path.startswith('/resources/'):
        db.close()
    return response

### index ############################################################
@app.route('/', methods=['GET'])
def index():
    return page.index.get()

### Cross Site Scripting (reflected) ############################################################
@app.route('/xssrf', methods=['POST'])
def xssrf():
    return page.index.post_xssrf()

### Cross Site Scripting (stored) ############################################################
@app.route('/xssst', methods=['POST'])
def xssst():
    return page.index.post_xssst()

### SQL Injection ############################################################
@app.route('/sqli', methods=['POST'])
def sqli():
    return page.index.post_sqli()

### Open Redirection ############################################################
@app.route('/oprd', methods=['POST', 'GET'])
def oprd():
    return page.index.post_oprd()



