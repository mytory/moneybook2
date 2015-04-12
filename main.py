#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
import time

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/template'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Details(ndb.Model):
    type = ndb.StringProperty()
    category = ndb.StringProperty()
    amount = ndb.IntegerProperty()
    memo = ndb.StringProperty()
    date = ndb.DateProperty()
    account = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class Accounts(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.StringProperty()
    whether_savings = ndb.BooleanProperty()
    in_balance = ndb.BooleanProperty()
    initial_amount = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class InitHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        webapp2.RequestHandler.__init__(self, request, response)
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))


class MainHandler(InitHandler):
    def get(self):
        self.redirect('register')


class RegisterHandler(InitHandler):
    def get(self):
        user = users.get_current_user()

        template_value = {
            'base_url': self.request.application_url,
            'user': user,
            'text': "안녕하세요"
        }

        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_value))

    def post(self):
        detail = Details()
        detail.type = self.request.get('type')
        detail.category = self.request.get('category')
        detail.amount = int(self.request.get('amount'))
        detail.memo = self.request.get('memo')
        detail.date = datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()
        detail.account = self.request.get('account')
        detail.put()
        self.redirect('register')


class ListHandler(InitHandler):
    def get(self):
        user = users.get_current_user()
        date = self.request.get('date')
        if not date:
            date = time.strftime('%Y-%m-%d')

        today = datetime.strptime(date, '%Y-%m-%d').date()
        tomorrow = (today + timedelta(days=1))
        yesterday = (today - timedelta(days=1))
        objs = Details\
            .query(Details.date >= today, Details.date < tomorrow)\
            .order(Details.date, -Details.created)\
            .fetch()

        template_value = {
            'tomorrow': tomorrow,
            'today': today,
            'yesterday': yesterday,
            'date': date,
            'objs': objs,
            'base_url': self.request.application_url,
            'user': user,
            'text': "안녕하세요"
        }

        template = JINJA_ENVIRONMENT.get_template('list.jinja2')
        self.response.write(template.render(template_value))


class AccountManageHandler(InitHandler):
    def get(self):
        user = users.get_current_user()
        id = self.request.get('id')
        # if not id:
        #     self.redirect('register')

        account = Accounts.get_by_id(id)

        template_value = {
            'account': account,
            'account_balance': 10000,
            'base_url': self.request.application_url,
            'user': user,
        }

        template = JINJA_ENVIRONMENT.get_template('account-manage.jinja2')
        self.response.write(template.render(template_value))


handler = [
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/list', ListHandler),
    ('/account-manage', AccountManageHandler),
]
app = webapp2.WSGIApplication(handler, debug=True)
