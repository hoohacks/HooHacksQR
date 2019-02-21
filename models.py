from flask import Flask
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(length=100))
    number = db.Column(db.Integer)
    checked_in = db.Column(db.Boolean, default=False)
    sat_breakfast = db.Column(db.Boolean, default=False)
    sat_lunch = db.Column(db.Boolean, default=False)
    sat_dinner = db.Column(db.Boolean, default=False)
    sun_breakfast = db.Column(db.Boolean, default=False)
    sun_lunch = db.Column(db.Boolean, default=False)
    dietary = db.Column(db.String(length=100))
    phone_number = db.Column(db.String(length=100))
    email = db.Column(db.String(length=100))

    def __init__(self, full_name, number, email, phone, dietary=""):
        self.full_name = full_name
        self.number = number
        self.email = email
        self.phone_number = phone
        self.dietary = dietary

    def reset(self):
        self.checked_in = False
        self.sat_breakfast = False
        self.sat_lunch = False
        self.sat_dinner = False
        self.sun_breakfast = False
        self.sun_lunch = False

    def __repr__(self):
        return '<Participant: {}>'.format(self.full_name)
