__author__ = 'Ian'


from flask import Flask

app = Flask(__name__) #'__main__'


@app.route('/')  # www.~~~~~.com/api/
def hello_method():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(port=4995)