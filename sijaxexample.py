# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: sijaxexample
@time:2022/7/14
@Author:majiaqin 170479
@Desc:Sijax应用程序
'''
import os
from flask import Flask, g
from flask_sijax import Sijax, route

path = os.path.join(',', os.path.dirname(__file__), 'static/js/sijax/')
app = Flask(__name__)

app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
Sijax(app)

@app.route('/')
def index():
    return 'Index'

@route(app, '/hello')
def hello():
    def say_hi(obj_response):
        obj_response.alert('Hi there!')
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()
    return _render_template('sijaxexample.html')

if __name__ == '__main__':
    app.run(debug=True)