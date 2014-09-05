# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
import os
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask.ext.script import Manager
from flask.ext.script import Shell

from flask.ext.migrate import Migrate, MigrateCommand
import os

from flask.ext.mail import Mail
from flask.ext.mail import Message

from threading import Thread

app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = 'fuboqing'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

mail = Mail(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {name}>'.format(name=self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)


# @app.route('/index')
# def index():
# mydict = {'key': 'fuboqing'}
# mylist = [1, 2, 3, 4]
#     myintvar = 2
#     myobj = MyObj()
#     return render_template('index.html', mydict=mydict, mylist=mylist, myintvar=myintvar, myobj=myobj)


class MyObj(object):
    def somemethod(self):
        return 'somemethod'


class Comment(object):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "I am comment with content: %s" % self.content


class User_Cp(object):
    def __repr__(self):
        return "I am User!"


@app.route('/user/<name>')
def user(name):
    user = User_Cp()
    comments = [Comment('1'), Comment('2'), Comment('3')]
    # return render_template('user.html', name=name, user=user, comments=comments)
    # return render_template('user_bt.html', name=name)
    return render_template('user_cp.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# @app.route('/')
# def index():
#     return render_template('index_cp.html', current_time=datetime.utcnow())

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('index_cp.html', form=form, name=name)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index_cp.html', form=form, name=session.get('name'))


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index_cp.html', form=form, name=session.get('name'))


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index_rp.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index_mp.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/init', methods=['GET'])
def init():
    db.create_all()
    return 'ok'


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context()))


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


if __name__ == '__main__':
    # app.run(debug=True)
    app.debug = True
    # manager.run()
    app.run()