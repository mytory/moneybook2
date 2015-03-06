#!/usr/bin/env python
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        # https://cloud.google.com/appengine/docs/python/gettingstartedpython27/templates
        self.response.headers['Content-Type'] = 'text/html'

        self.response.write('<h1>Hello world!</h1>')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
