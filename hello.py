# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, render_template

app = Flask(__name__)


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


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)