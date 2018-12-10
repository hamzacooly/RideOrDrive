from flask_login import UserMixin, LoginManager
from werkzeug.security import check_password_hash
from .flaskapp import app
from .db import appDB

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):

    def __init__(self, username, password, history):
        self.id = username
        self.pw_hash = password
        self.history = history

    def add_history_item(self, item):
        self.history.append(item)
        appDB.users.update({'_id':self.id}, {'$push':{'history':item}})

    def get_history(self):
        return self.history

    @staticmethod
    def query_user(id):
        user = appDB.users.find_one({'_id': id})
        if user:
            return User(user['_id'], user['password'], user['history'])
        else:
            return None

def check_password(the_hash, password):
    return check_password_hash(the_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query_user(id)