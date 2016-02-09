import logging
import time

import hashlib

import webapp2
import jinja2

import json
import os

from models import *
from helpers import *
from seeds import get_videos
from seeds import get_users

from webapp2_extras import sessions

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

log = logging.getLogger(__name__)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class MainHandler(Handler):
    def get(self):
        q = Video.query().order(Video.display_order, Video.date)
        videos_db = q.fetch(100)
        self.render('index.html',videos_db=videos_db)

### These are the handlers that deal with Admin functions

class SigninHandler(Handler):
    def get(self):
        self.render('signin.html')
    def post(self):
        username = self.request.get('username')
        pw = self.request.get('pw')
        if User.login(username,pw):
            self.session['username'] = username
        self.redirect('/admin')

class AdminHandler(Handler):
    @require_user
    def get(self):
        self.render('adder.html')

    @require_user
    def post(self):
        title = self.request.get('title')
        code = self.request.get('code')
        year = self.request.get('year')
        qry = Video.query(Video.video_id == code).fetch(1)
        if qry:
            error = "Video with that ID already on page"
            self.render('adder.html',error=error)
        else:
            new_video = Video(
                video_id=code,
                title=title,
                year=year
            )
            new_video.put()
            time.sleep(1)
            self.redirect('/admin')

class VideoLister(Handler):
    @require_user
    def get(self):
        videos_db = Video.query().order(Video.display_order, Video.date)
        self.render('list.html',videos_db=videos_db)

    @require_user
    def post(self):
        order = self.request.get('order')
        order = order.split(',')
        for i, vid_id in enumerate(order):
            logging.info(vid_id)
            v = Video.query(Video.video_id == vid_id).get()
            v.display_order = i
            v.put()
        self.write('OK')

class DeleteHandler(Handler):
    @require_user
    def get(self):
        videos = Video.query().order(Video.date)
        self.render('deleter.html',videos=videos)

    @require_user
    def post(self):
        unwanted = self.request.get_all('unwanted')
        for i in unwanted:
            i = int(i)
            video = Video.get_by_id(i)
            video.key.delete()
        time.sleep(1)
        self.redirect('/list')


### These are pretty  much just for testing

class DebugHandler(Handler):
    def get(self):
        logging.info("hello, world!")
        videos = Video.query()
        users = User.query()
        self.render('debugger.html',videos=videos, users=users)

class DropHandler(Handler):
    def get(self,table_name):
        ref = {
            'users':User,
            'videos':Video
            }
        db = ref[table_name].query()
        for entry in db:
            entry.key.delete()
        self.write('All %s deleted' % table_name)

class SeedHandler(Handler):
    def get(self):
        videos = get_videos()
        for video in videos:
            title = video['title']
            code = video['video_id']
            year = video['year']
            qry = Video.query(Video.video_id == code).fetch(1)
            if not qry:
                new_video = Video(video_id=code,
                title=title,
                year=year)
                new_video.put()
        time.sleep(1)
        self.redirect('/')

class AddUsers(Handler):
    def get(self):
        users = get_users()
        for user in users:
            username = user['username']
            email = user['email']
            pw = make_pw_hash(username,user['pw'])
            u = User.query(User.username == username).get()
            if not u:
                new_user = User(username = username,
                email = email,
                pw_hash = pw)
                new_user.put()
        self.write('Added the users')
