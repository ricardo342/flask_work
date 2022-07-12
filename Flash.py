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
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from flask_wtf import Form
from wtforms import TextAreaField
import os

app = Flask(__name__)
app.secret_key = 'random string'
app.config['UPLOAD_FOLDER'] = 'upload/'
Mail(app=None)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Hello', sender='yourId@gmail.com',
                  recipients=['id1@gmail.com'])
    msg.body = 'This is the email body'
    mail.send(msg)
    return 'Sent'

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

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file uploaded successfully'
    else:
        return render_template('upload.html')

class ContactForm(Form):
    name = TextAreaField("Name Of Student")

@app.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)