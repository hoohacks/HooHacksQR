from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
import random
import sys
from database import db_session
import json
from werkzeug.utils import secure_filename
from config import Config
from datetime import datetime
from flask_admin import Admin
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView as MV
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

try:
    if os.environ['FLASK_ENV'] == "development":
        import settings
        app.config['APP_SETTINGS'] = settings.APP_SETTINGS
        app.secret_key = settings.SECRET_KEY
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
        app.config['BASIC_AUTH_USERNAME'] = settings.ADMIN_USERNAME
        app.config['BASIC_AUTH_PASSWORD'] = settings.ADMIN_PASSWORD
except:
    app.config['APP_SETTINGS'] = os.environ['APP_SETTINGS']
    app.secret_key = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['BASIC_AUTH_USERNAME'] = os.environ['ADMIN_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['ADMIN_PASSWORD']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)

class ModelView(MV):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            message, 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

from models import Participant

admin = Admin(app, name='HooHacks', template_mode='bootstrap3')
admin.add_view(ModelView(Participant, db.session))

@app.route('/', methods=["GET", "POST"])
@basic_auth.required
def html_page():
    return render_template("page.html")

@app.route('/req/<typ>/<num>', methods=["GET", "POST"])
def change_request(typ, num):
    p = Participant.query.filter_by(number=num)
    if p.count() == 0:
        return jsonify({
            "approved": False,
            "error": "ERROR - no user found"
        })
    else:
        p = p.first()
    err = ""
    if typ == "check-in":
        if p.checked_in:
            err = "already checked in"
        p.checked_in = True
    elif typ == "sat-breakfast":
        if p.sat_breakfast:
            err = "already ate Saturday breakfast"
        p.sat_breakfast = True
    elif typ == "sat-lunch":
        if p.sat_lunch:
            err = "already ate Saturday lunch"
        p.sat_lunch = True
    elif typ == "sat-dinner":
        if p.sat_dinner:
            err = "already ate Saturday dinner"
        p.sat_dinner = True
    elif typ == "sun-breakfast":
        if p.sun_breakfast:
            err = "already ate Sunday breakfast"
        p.sun_breakfast = True
    elif typ == "sun-lunch":
        if p.sun_lunch:
            err = "already ate Sunday lunch"
        p.sun_lunch = True
    else:
        return jsonify({
            "name": p.full_name,
            "approved": False,
            "vegetarian": p.vegetarian,
            "halal": p.halal,
            "nut": p.nut,
            "vegan": p.vegan,
            "error": "ERROR - request type not found"
        })
    if not err == "":
         return jsonify({
             "approved": False,
             "error": "ERROR - " + p.full_name + " has " + err,
         })
    db.session.add(p)
    db.session.commit()
    return jsonify({
        "name": p.full_name,
        "approved": True,
        "vegetarian": p.vegetarian,
        "halal": p.halal,
        "nut": p.nut,
        "vegan": p.vegan,
        "error": "none"
    })

if __name__ == '__main__':
    app.run()
