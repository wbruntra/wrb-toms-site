import hashlib

def make_pw_hash(name, pw):
    h = hashlib.sha256(name + pw).hexdigest()
    return '%s' % (h)

def valid_pw(name, password, h):
    return h == make_pw_hash(name, password)

def require_user(old_func):
    def new_function(self):
        if not self.session.get('username'):
            self.redirect('/signin')
        old_func(self)
    return new_function
