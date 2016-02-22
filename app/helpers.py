import hashlib

def get_salt():
    chars = [chr(x) for x in (range(65,91)+range(97,123))]
    result = ''
    for i in range(5):
        result = result + random.choice(chars)
    return result

def make_pw_hash(name, pw,salt):
    h = hashlib.sha256(name+pw+salt).hexdigest()
    return '%s' % (h)

def valid_pw(name, password, salt, h):
    return h == make_pw_hash(name, password, salt)

def require_user(old_func):
    def new_function(self):
        if not self.session.get('username'):
            self.redirect('/signin')
        old_func(self)
    return new_function
