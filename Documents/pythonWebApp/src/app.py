from flask import make_response

from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User
from flask import Flask, render_template, request, session

__author__ = 'Ian'


app = Flask(__name__)  # '__main__'
app.secret_key = "inorris372"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])  # www.~~~~~.com/api/
def login_template():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        return render_template('profile.html', email=session['email'])
    else:
        if User.has_registered(email):
            print("Incorrect password - please try again.")
        else:
            print("You are not registered!  Please register or"
                  "verify your login information and try again.")
        session['email'] = None
        return render_template('login.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    if User.has_registered(email):
        print("You already have an account! Please enter your password.")
        return render_template('login.html')
    else:
        User.register(email, password)
        return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>', methods=['GET', 'POST'])
@app.route('/blogs/', methods=['GET', 'POST'])
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()

    return render_template('user_blogs.html', blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['GET', 'POST'])
def create_new_blog():
    if request.method == "GET":
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>', methods=['GET', 'POST'])
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


if __name__ == '__main__':
    app.run(port=4995)
