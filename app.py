from flask import Flask, redirect
from flask import render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    greeting = "Hello there, Need a Drink ?"
    return render_template('index.html', greet=greeting)


@app.route('/loading')
def loading():
    return render_template('loading.html')


@app.route('/checkUser')
def checkUser():
    f = open("user.txt", "r")
    username = f.readline()
    f.close()
    if username:
        print(username)
        address = '/user/' + username
        return redirect(address)
    else:
        return render_template('newuser.html')


@app.route('/user/<username>')
def new_user(username):
    return render_template('user.html')



if __name__ == '__main__':
    app.run(debug=True)
