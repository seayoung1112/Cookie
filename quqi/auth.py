# -*- coding: utf-8 -*-
from flask import session, request, g, redirect, url_for
from models import User
from functools import wraps
from core import app

@app.before_request
def init_user():
    if '__auth_user' in session:
        g.user = User.get(session['__auth_user'])
    else:
        g.user = None

def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.user is None:        
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def login(user):
    id = user.id
    if id is None:
        raise NameError('user id is none')
    session['__auth_user'] = id    

def logout(user):
    session.pop('__auth_user', None)

def check_password(username, password):
    pass
    
    