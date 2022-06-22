from flask import Flask, url_for, request, render_template,\
    make_response, abort, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#     else:
#         error = 'Invalid username/password'
#     return render_template('login.html', error=error)

@app.route('/index')
def index():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('username', 'the_username')
    username = request.cookies.get('username')
    return username

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User {0}'.format(username)

'''有三种转换器int&float&path'''
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {0}'.format(post_id)

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['the file']
#         f.save('/var/www/uploads/'+secure_filename(f.filename))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('show_user_profile', username='majiaqin'))
    print(url_for('show_post', post_id=666))
    print(url_for('projects', next='sss'))
    print(url_for('about', next='/'))
    print(url_for('static', filename='style.css'))

with app.test_request_context('/hello', method='POST'):
    assert request.path == '/hello'
    assert request.method == 'POST'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
