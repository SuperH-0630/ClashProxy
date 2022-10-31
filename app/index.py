from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

from .logger import Logger
from clash import METHODS, add_direct_rule_to_sql


index = Blueprint("base", __name__)


class AddRuleForm(FlaskForm):
    method = SelectField("规则方式", description="规则命中方式", validators=[DataRequired("必须设定规则方式")])
    address = StringField("规则", description="规则", validators=[DataRequired("必须设定规则")])
    no_resolve = BooleanField("no-resolve", description="选择no-resolve")
    submit = SubmitField("提交")

    def __init__(self):
        super(AddRuleForm, self).__init__()

        self.method.choices = METHODS
        self.method.coerce = str
        self.method.default = METHODS[0]


def __load_index_page(form:AddRuleForm = None):
    if not form:
        form = AddRuleForm()

    Logger.print_load_page_log("index")
    return render_template("index/index.html", form=form)


@index.route("/")
@login_required
def index_page():
    return __load_index_page()


@index.route("/add-rule", methods=["GET", "POST"])
@login_required
def add_rule_page():
    form = AddRuleForm()
    if form.validate_on_submit():
        res = add_direct_rule_to_sql(form.method.data, form.address.data, None, form.no_resolve.data)
        if res:
            flash("新增规则成功")
        else:
            flash("不可重复新增规则")
        return redirect(url_for("base.index_page"))
    return __load_index_page(form)
