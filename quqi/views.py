# -*- coding: utf-8 -*-
from core import app
from config import SITE_PATH, MEDIA
from auth import auth, login as auth_login, logout as auth_logout
from flask import redirect, url_for, render_template, g, request, jsonify
from models import User, Product
from forms import ProductForm
from sqlalchemy import and_

from renren_api import *

@app.route('/')
def home():
    products=Product.query.all()
    return render_template('home.html', products=products)

### login related views
@app.route('/login', methods=['GET', 'POST'])
def login():
    #for test use
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = User.query.filter(User.name == request.form['name']).first()
        auth_login(user)
        return redirect('/')
    #redirect to loginByRenren, this function should be enhanced later
#    return redirect(url_for('login_by_renren'))

@app.route('/loginbyrenren')
def login_by_renren():
    verification_code = request.args.get("code")
    args = dict(client_id=RENREN_APP_API_KEY, redirect_uri='http://www.oxxooox.com:5000/loginbyrenren')   
    error = request.args.get("error")
    if error:
        args["error"] = error
        args["error_description"] = request.args.get("error_description")
        args["error_uri"] = request.args.get("error_uri")

        args = dict(error=args)
        return args["error_description"]
    elif verification_code:
        args["client_secret"] = RENREN_APP_SECRET_KEY
        args["code"] = verification_code
        args["grant_type"] = "authorization_code"
        response = urllib.urlopen(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args)).read()
        access_token = parse_json(response)["access_token"]        
        '''Obtain session key from the Resource Service.'''
        session_key_request_args = {"oauth_token": access_token}
        response = urllib.urlopen(RENREN_SESSION_KEY_URI + "?" + urllib.urlencode(session_key_request_args)).read()
        session_key = str(parse_json(response)["renren_token"]["session_key"])
        
        '''Requesting the Renren API Server obtain the user's base info.'''
        params = {"method": "users.getInfo", "fields": "name,tinyurl"}
        api_client = RenRenAPIClient(session_key, RENREN_APP_API_KEY, RENREN_APP_SECRET_KEY)
        response = api_client.request(params);
        if type(response) is list:
            response = response[0]
        user_id = response["uid"]
        name = response["name"]
        avatar = response["tinyurl"]

        renren_user = RenrenUser.query.filter(RenrenUser.renren_id == user_id).first()
        if renren_user is None:
            renren_user = RenrenUser(name, avatar, user_id)
            renren_user.save()
        elif renren_user.portrait != avatar:
            renren_user.portrait = avatar
            renren_user.save()
        auth_login(renren_user)

        return redirect("/")
    else:
        args["response_type"] = "code"
        args["scope"] = "publish_feed email status_update"
        return redirect(
            RENREN_AUTHORIZATION_URI + "?" +
            urllib.urlencode(args))

@app.route('/logout')
@auth
def logout():
    auth_logout(g.user)
    return redirect(url_for('home'))
### login related views

### product related views
@app.route('/product/share', methods=['GET', 'POST'])
@auth
def share():
    if request.method == 'GET':
        form = ProductForm()
    else:
        form = ProductForm(request.form)
        if form.validate():
            if form.create_product(g.user) is not None:            
                return redirect(url_for('home'))    
    return render_template('share_product.html', form=form)

@app.route('/product/uploadPicture', methods=['POST'])
@auth
def upload_picture():
    file = request.files['picture']
    if file:
        path = MEDIA + 'user_tmp_img/' + str(g.user.id) + '_tmp_cover.png'
        file.save(SITE_PATH + path)
    return path + '?' + (os.urandom(6)).encode('hex')
    
### product related views
