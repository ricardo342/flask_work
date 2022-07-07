# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: flaskr
@time:2022/6/23
@Author:majiaqin 170479
@Desc:Flask 应用设置代码
'''

import os
import sqlite3
from flask import Flask,request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__, template_folder='templates')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/hello/<name>')
def hello_name(name):
    return 'hello {0}'.format(name)

@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number {0}'.format(postID)

@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number {0}'.format(revNo)

def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_name'))
    else:
        return redirect(url_for('show_blog'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name):
    return 'welcome {0}'.format(name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(1)
        user = request.form['name']
        return redirect(url_for('hello_user', name=user))
    else:
        print(2)
        user = request.args.get('name')
        return redirect(url_for('success', name=user))

@app.route('/student')
def student():
    return render_template('student.html')

def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)