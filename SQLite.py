# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: SQLite
@time:2022/7/12
@Author:majiaqin 170479
@Desc:
'''

import sqlite3
from flask import g, Flask, render_template, request
from contextlib import closing

app = Flask(__name__)
DATABASE = '/path/to/database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row))
          for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/addrec', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, pin) \
                            VALUES (?, ?, ?, ?)", (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template('result.html', msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template('list.html', rows=rows)