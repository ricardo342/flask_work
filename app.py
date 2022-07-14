# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: flaskr
@time:2022/6/23
@Author:majiaqin 170479
@Desc:Flask 应用设置代码
'''

from flask import Flask, request, flash, url_for, redirect, render_template, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask.views import View, MethodView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

class ListView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)

class UserView(ListView):
    def get_template_name(self):
        return 'users.html'

    def get_objects(self):
        return User.query.all()

class MyView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            pass

app.add_url_rule('/myview', view_func=MyView.as_view('myview'))

def user_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not g.user:
            abort(401)
        return f(*args, **kwargs)
    return decorator

view = user_required(UserAPI.as_view('users'))
app.add_url_rule('/user/', view_func=view)

class UserAPI(MethodView):
    decorators = [user_required]

app.add_url_rule('/user/', view_func=UserAPI.as_view('users'))

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, default={pk: None},
                     view_func=view_func,
                     methods=['GET', ])
    app.add_url_rule(url, view_func=view_func,
                     methods=['POST', ])
    app.add_url_rule('{0}<{1}:{2}>'.format(url, pk_type, pk),
                     view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
register_api(UserAPI, 'user_api', '/users/', pk='user_id')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)