from src.common.database import Database
from src.models.user import User
from flask import Flask, render_template, request, session

__author__ = 'Ian'


app = Flask(__name__)  # '__main__'
app.secret_key = "inorris372"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')  # www.~~~~~.com/api/
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login')
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        login_template()
        print("The email address that you entered was either invalid"
              "or has not yet been registered with the Blogosphere.")

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run(port=4995)
