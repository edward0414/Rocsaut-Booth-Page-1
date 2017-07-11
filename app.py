from flask import Flask, flash, redirect, render_template, request, g, session, url_for
from functools import wraps
import os
import sqlite3

app = Flask(__name__)

database = 'ROCSAUT.db'

#Make username a global variable?
#username = ""

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
#Add username to this page somehow

    try:
        g.db = sqlite3.connect(database)
        g.db.row_factory = sqlite3.Row

        #extract from tables Transcation and Member
        cur = g.db.execute('select * from Transcation')
        orders = cur.fetchall()
        cur = g.db.execute('select * from Member')
        members = cur.fetchall()

        g.db.close()

    except sqlite3.OperationalError:
        flash("You have no database")

    username = "admin"
    return render_template('welcome.html', user=username, orders=orders, members=members)


@app.route('/addTranscation', methods=['GET', 'POST'])
def addTranscation():
    error = None
    if request.method == 'POST':
        try:
            staffID = request.form['staffID']
            cardnum = request.form['cardnum']
            memberID = request.form['memberID']
            date = request.form['date']
            description = request.form['description']
            income = request.form['income']
            expense = request.form['expense']

            g.db = sqlite3.connect(database)

            #auto update the balance
            #extract the balance of the last entry
            #gonna have problems when modifying the data?
            cur = g.db.execute('SELECT Max(TranscationID), Balance FROM Transcation')
            for row in cur.fetchall():
                balance = row[1]
            balance = int(balance) + int(income) - int(expense)

            
            cur = g.db.execute('INSERT INTO Transcation (StaffID,CardNum,MemberID,Date,Description,Income,Expense,Balance) VALUES (?,?,?,?,?,?,?,?)',(staffID,cardnum,memberID,date,description,income,expense,balance))
            g.db.commit()
            g.db.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except sqlite3.OperationalError:
            error = "Fail to insert new data"


    return render_template('addTranscation.html', error=error)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupStaff', methods=['GET', 'POST'])
def signupStaff():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            memberID = request.form['memberID']
            cardnum = request.form['cardnum']
            username = request.form['username']
            password = request.form['password']
            position = request.form['position']

            g.db = sqlite3.connect(database)
            
            cur = g.db.execute('INSERT INTO Staff (MemberID,CardNum,Username,Password,Position) VALUES (?,?,?,?,?)',(memberID,cardnum,username,password,position))
            g.db.commit()
            g.db.close()
            error = "Sign up successfully!"
            return redirect(url_for('login'))

        except sqlite3.OperationalError:
            error = "Fail to sign up."

    return render_template('signupStaff.html', error=error)



@app.route('/signupMember', methods=['GET', 'POST'])
def signupMember():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            cardnum = request.form['cardnum']
            fname = request.form['fname']
            lname = request.form['lname']
            program = request.form['program']
            email = request.form['email']
            year = request.form['year']

            g.db = sqlite3.connect(database)
            
            cur = g.db.execute('INSERT INTO Member (CardNum,FirstName,LastName,Program,Email,Year) VALUES (?,?,?,?,?,?)',(cardnum,fname,lname,program,email,year))
            g.db.commit()
            g.db.close()
            error = "Sign up successfully!"

        except sqlite3.OperationalError:
            error = "Fail to sign up."

    return render_template('signupMember.html', error=error)



@app.route('/login', methods=['GET','POST'])
def login():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']

            #extract the password from the database
            g.db = sqlite3.connect(database)
            cur = g.db.execute("SELECT Password FROM Staff WHERE Username='{}'".format(username))
            for row in cur.fetchall():
                password = row[0]
            g.db.close()

            #check password
            if request.form['password'] == password:
                session['logged_in'] = True
                return redirect(url_for('welcome'))
            else:
                error = 'Invalid credentials. Please try again.'

        except sqlite3.OperationalError:
            error = "Fail to log in."

    return render_template('login.html', error=error)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have just logged out')
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
