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
    render_template, flash, make_response

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'

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
    if 'username' in session:
        username = session['username']
        return '登录用户名是:' + username + '<br>' + \
"<b><a href = '/logout'>点击这里注销</a></b>"

    return "您暂未登录， <br><a href = '/login'></b>" + \
"点击这里登录</b></a>"

@app.route('/success/<name>')
def success(name):
    return 'welcome {0}'.format(name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/result')
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result=result)

@app.route('/set_cookies')
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("w3cschool", "w3cschool", max_age=3600)
    return resp

@app.route('/get_cookies')
def get_cookie():
    cookie_1 = request.cookies.get("w3cschool")
    return cookie_1

@app.route('/delete_cookies')
def delete_cookie():
    resp = make_response('del success')
    resp.delete_cookie("w3cschool")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)