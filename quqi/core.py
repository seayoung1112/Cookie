# -*- coding: utf-8 -*-
from flask import Flask, request, session, abort, Markup
import hashlib
from random import randrange
from config import SECRET_KEY
app = Flask(__name__)
app.secret_key = SECRET_KEY
import views
from database import db_session

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response

### csrf protection
@app.before_request
def csrf_protect():
    if request.method == "POST":
        #token = session.pop('_csrf_token', None)
        token = session.get('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            print token
            print request.form.get('_csrf_token')
            abort(403)

_MAX_CSRF_KEY = 18446744073709551616L

def generate_csrf_token():
    if '_csrf_token' not in session:
        token = hashlib.md5("%s%s" % (randrange(0, _MAX_CSRF_KEY), app.secret_key)).hexdigest()
        session['_csrf_token'] = token
    return Markup(ur'<input name="_csrf_token" type="hidden" value="%s" id="_csrf_token"/>' % session['_csrf_token']) 

app.jinja_env.globals['csrf_token'] = generate_csrf_token   