from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# from flask.ext.heroku import Heroku

import random
#import settings
import sys
from database import db_session
import json
from werkzeug.utils import secure_filename
from config import Config
from datetime import datetime

app = Flask(__name__)

app.config['APP_SETTINGS'] = os.environ['APP_SETTINGS']
#app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #settings.TRACK_MODIFICATIONS
app.secret_key = os.environ['SECRET_KEY']

# os.environ["APP_SETTINGS"] =
#os.environ["DATABASE_URL"] = settings.DB_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
heroku = Heroku(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import Participant

@app.route('/', methods=["GET", "POST"])
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
