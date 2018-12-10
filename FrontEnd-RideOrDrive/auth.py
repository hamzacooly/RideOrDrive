from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapp import appDB

class User(UserMixin):

    def __init__(self, username, password, history):
        self.username = username
        self.set_password(password)
        self.history = history

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    
    def add_history_item(self, item):
        self.history.append(item)
        appDB.users[self.username]['history'].insert(item)
    
    def get_history(self):
        return self.history
    
    @staticmethod
    def query_user(id):
        user = appDB.users.find_one({'_id': id})
        if user:
            return User(user._id, user.password, user.history)
        else:
            return None