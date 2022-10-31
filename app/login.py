from flask_login import LoginManager
from .user import User


login = LoginManager()
login.login_view = "auth.login_page"


@login.user_loader
def user_loader(id_):
    user = User()
    if user.check_id(id_):
        return user
    return None
