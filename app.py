from flask import Flask, flash, redirect, render_template, request, g, session, url_for
from functools import wraps
import os
import sqlite3

app = Flask(__name__)

app.database = "sample.db"

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/welcome')
@login_required
def welcome():
    posts = []
    try:
        g.db = connect_db()
        cur = g.db.execute('select * from posts')
        posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
        g.db.close()
    except sqlite3.OperationalError:
        flash("You have no database")
        
    username = 'admin'
    return render_template('welcome.html', username=username, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have just logged out')
    return redirect(url_for('home'))

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    fname = request.form['inputfName']
    lname = request.form['inputlName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
