from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
import os
from flaskext.mysql import MySQL

app = Flask(__name__)


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '7782941578q'
app.config['MYSQL_DATABASE_DB'] = 'Order'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


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
    return render_template('welcome.html', user=user, orders=orders, members=members)


@app.route('/addTranscation', methods=['GET', 'POST'])
@login_required
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


@app.route('/signupMember', methods=['GET', 'POST'])
def signupMember():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            campus = request.form['campus']
            cardnum = request.form['cardNum']
            stunum = request.form['stuNum']
            fname = request.form['fName']
            lname = request.form['lName']
            cname = request.form['cName']
            if (cname == ""):
                cname = 'NULL'
            gender = request.form['gender']
            byear = request.form['bYear']
            bmonth = request.form['bMonth']
            bdate = request.form['bDate']
            email = request.form['email']
            phone = request.form['phone']
            program = request.form['program']
            oprogram = request.form['oProgram']
            if oprogram:
                program = oprogram
            year = request.form['year']

            conn = mysql.connect()
            cursor = conn.cursor()

            
            cursor.execute("SELECT * FROM member WHERE memberID={}".format(cardnum))
            result1 = cursor.fetchone()
            cursor.execute("SELECT * FROM member WHERE studentID='{}'".format(stunum))
            result2 = cursor.fetchone()

            if result1 is not None:
            # prevent the user from entering the same member card number
                error= "The member card number entered is already in the system. Please use a different one."
                conn.close()
                raise Exception(error)

            elif result2 is not None:
            # prevent the user from entering the same student number
                error= "The student number entered is already in the system. You are already a member."
                conn.close()
                raise Exception(error)

            else:
                # (cardNum,stuNum,fName,lName,cName,phone,email,gender,birth,campus,year,program,7xNuLL)
                query = "INSERT INTO member VALUES ({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}',{12},'{13}', {14}, {15}, {16}, {17}, {18}, {19}, {20});".format(cardnum,stunum,fname,lname,cname,phone,email,gender,byear,bmonth,bdate,campus,year,program,'NULL','NULL','NULL','NULL','NULL','NULL','NULL')
                cursor.execute(query)

                conn.commit()
                conn.close()
                flash("Sign up successfully!")
                return redirect(url_for('signupMember'))

        except Exception as e:
            print('fail')
            error = "Fail to sign up. " + str(e.args[0])

    return render_template('signupMember.html', error=error)



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



@app.route('/login', methods=['GET','POST'])
def login():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            global user
            username = request.form['username']
            user = username

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
