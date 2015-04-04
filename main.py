#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime

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
        detail.date = datetime.strptime(self.request.get('date'), '%Y-%m-%d')
        detail.put()
        self.redirect('register')


app = webapp2.WSGIApplication([('/', MainHandler), ('/register', RegisterHandler), ], debug=True)
