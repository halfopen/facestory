# coding:utf-8

"""
    系统管理

"""

from flask import redirect, url_for, request
from wtforms import form, fields, validators
from flask_admin import helpers, AdminIndexView, expose, Admin
from flask_admin.contrib import sqla
from models import *
from flask_babelex import *
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from constant import *


def add_admin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    class LoginForm(form.Form):
        login = fields.StringField(validators=[validators.required()])
        password = fields.PasswordField(validators=[validators.required()])

        def validate_login(self, field):
            user = self.get_user()

            if user is None:
                raise validators.ValidationError('Invalid user')

            # we're comparing the plaintext pw with the the hash from the db
            print(user.passwd, self.password.data, generate_password_hash(user.passwd))
            if not check_password_hash(user.passwd, self.password.data):
                # to compare plain text passwords use
                # if user.password != self.password.data:
                raise validators.ValidationError('Invalid password')

        def get_user(self):
            return db.session.query(User).filter_by(login=self.login.data).first()

    class BaseAdminIndexView(AdminIndexView):
        @expose('/')
        def index(self):
            if not current_user.is_authenticated():
                return redirect(url_for('.login_view'))
            return super(BaseAdminIndexView, self).index()

        @expose('/login/', methods=('GET', 'POST'))
        def login_view(self):
            # handle user login
            form = LoginForm(request.form)
            if helpers.validate_form_on_submit(form):
                user = form.get_user()
                login_user(user)

            if current_user.is_authenticated():
                return redirect(url_for('.index'))
            self._template_args['form'] = form
            return super(BaseAdminIndexView, self).index()

        @expose('/logout/')
        def logout_view(self):
            logout_user()
            return redirect(url_for('.index'))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    class MyBaseModelView(sqla.ModelView):
        can_export = True
        can_view_details = True
        column_labels = COLUMN_LABELS

        def is_accessible(self):
            return current_user.is_authenticated()

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('.login_view'))

    class FaceStoryView(MyBaseModelView):
        column_exclude_list = ['avatar_url', 'story_json']  # 不显示的区域
        column_searchable_list = ['story_json']
        column_filters = ['openid']
        can_export = True

    class UserInfoView(MyBaseModelView):
        pass

    class LogView(MyBaseModelView):
        pass

    Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    app.config['BASIC_AUTH_USERNAME'] = 'john'
    app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
    admin = Admin(app, name=u'后台管理系统', index_view=BaseAdminIndexView())
    admin.add_view(UserInfoView(UserInfo, db.session, name=u"微信用户"))
    admin.add_view(FaceStoryView(FaceStory, db.session, name=u"自拍记录"))
    admin.add_view(LogView(Log, db.session, name=u"操作日志"))
    return app