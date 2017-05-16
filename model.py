#   Copyright 2017 Massachusetts Open Cloud
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import ConfigParser

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

import wsgi

from config import set_config_file


config = ConfigParser.ConfigParser()
config.read(set_config_file('settings.ini'))
database_uri = config.get('database', 'uri')
wsgi.app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(wsgi.app)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    request_created = db.Column(db.TIMESTAMP, nullable=False)
    helpdesk_ticket = db.Column(db.TIMESTAMP, nullable=True)
    reminder = db.Column(db.TIMESTAMP, nullable=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.String(64), unique=True)
    project_id = db.Column(db.String(64), unique=True)
    quota_change = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, email, user_id=None,
                 project_id=None, quota_change=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = user_id
        self.project_id = project_id
        self.quota_change = quota_change

#    def __repr__(self):
#        return '<User %r, Token %r>' % (self.user_id, self.token)

#    @staticmethod
#    def find(**kwargs):
#        return Request.query.filter_by(**kwargs).first()


class NewUser(db.Model):
    __tablename__ = 'new_users'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(
        db.Integer, db.ForeignKey('requests.id'), nullable=False)
    request = relationship(Request)
    username = db.Column(db.String(64), nullable=False)
    organization = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    sponsor = db.Column(db.String(64), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
     
    def __init__(self, request, username, organization, role, sponsor, pin,
                 comment):
        self.request = request
        self.username = username
        self.organization = organization
        self.role = role
        self.sponsor = sponsor
        self.pin = pin
        self.comment = comment


class NewProject(db.Model):
    __tablename__ = 'new_projects'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(
        db.Integer, db.ForeignKey('requests.id'), nullable=False)
    request = relationship(Request)
    project_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    add_users = db.Column(db.String(255), nullable=False)
    
    def __init__(self, request, project_name, description, add_users):
        self.request = request
        self.project_name = project_name
        self.description = description
        self.add_users = add_users


db.create_all()
