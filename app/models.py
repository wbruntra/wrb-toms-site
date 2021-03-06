from google.appengine.ext import ndb
import hashlib
from helpers import *

class Video(ndb.Model):
    video_id = ndb.StringProperty()
    title = ndb.StringProperty()
    year = ndb.StringProperty()
    display_order = ndb.IntegerProperty(default=999)
    date = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    username = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    salt = ndb.StringProperty(required=True)

    @classmethod
    def by_name(cls, name):
        u = User.query(User.username == name).get()
        return u

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.salt, u.pw_hash):
            return u
