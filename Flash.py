# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: Flash
@time:2022/7/7
@Author:majiaqin 170479
@Desc:Flask 消息闪现示例
'''
from flask import Flask, flash, redirect, render_template, \
request, url_for

app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)