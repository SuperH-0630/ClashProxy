from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from .logger import Logger
from .user import User
from config import conf

auth = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    username = StringField("用户名", description="用户名", validators=[DataRequired("必须填写用户名")])
    passwd = PasswordField("密码", description="密码", validators=[DataRequired("必须填写密码")])
    submit = SubmitField("登录")


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if not current_user.is_anonymous:
        flash("不能重复登录")
        return redirect(url_for("base.index_page"))

    form = LoginForm()
    if form.validate_on_submit():
        if conf["USERNAME"] == form.username.data and conf["PASSWD"] == form.passwd.data:
            login_user(User(), remember=True)
            flash("登陆成功")
            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('base.index_page')
            Logger.print_user_opt_success_log(f"login {form.username.data}")
            return redirect(next_page)
        else:
            flash("账号验证失败")
            Logger.print_user_opt_fail_log(f"login {form.username.data}")
            return redirect(url_for("auth.login_page"))
    Logger.print_load_page_log("login")
    return render_template("auth/login.html", form=form)




@auth.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("退出登录成功")
    Logger.print_user_opt_success_log(f"logout")
    return redirect(url_for("auth.login_page"))
