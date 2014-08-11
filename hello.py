# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/index')
def index():
    mydict = {'key': 'fuboqing'}
    mylist = [1, 2, 3, 4]
    myintvar = 2
    myobj = MyObj()
    return render_template('index.html', mydict=mydict, mylist=mylist, myintvar=myintvar, myobj=myobj)


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
    return render_template('user_bt.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)