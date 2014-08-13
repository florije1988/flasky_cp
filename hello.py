# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)


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


@app.route('/')
def index():
    return render_template('index_cp.html', current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True)