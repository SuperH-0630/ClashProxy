from flask_login import UserMixin

from config import conf


class User(UserMixin):
    def __init__(self):
        super(User, self).__init__()
        self.id = conf["ID"]

    def check_id(self, id_):
        return self.id == id_

