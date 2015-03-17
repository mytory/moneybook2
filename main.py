#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
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
            'base_url': 'http://' + self.request.host,
            'user': user,
            'text': "안녕하세요"
        }

        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_value))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
], debug=True)
