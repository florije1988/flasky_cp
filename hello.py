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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuboqing'

bootstrap = Bootstrap(app)
moment = Moment(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role {name}>'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User {username}>'.format(self.username)


# @app.route('/index')
# def index():
#     mydict = {'key': 'fuboqing'}
#     mylist = [1, 2, 3, 4]
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


class User(object):

    def __repr__(self):
        return "I am User!"


@app.route('/user/<name>')
def user(name):
    user = User()
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index_cp.html', form=form, name=session.get('name'))


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

if __name__ == '__main__':
    app.run(debug=True)