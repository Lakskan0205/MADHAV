import email
from flask import Flask, render_template, request
import ibm_db
from flask_mail import Mail, Message
from random import randint

connectionstring="DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;PROTOCOL=TCPIP;UID=kmy46098;PWD=PN0aG7meNBbB7HH1;SECURITY=SSL;"
connection = ibm_db.connect(connectionstring, '', '')

app = Flask(__name__)
mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = '2k19cse052@kiot.ac.in'
app.config['MAIL_PASSWORD'] = 'nxgknupghjjodabq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route('/verification', methods=["POST","GET"])
def verify():

    if request.method == 'POST':
        global first_name
        global last_name
        global useremail
        global password
        global email
        global otp

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        useremail = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM User WHERE email =?"
        stmt = ibm_db.prepare(connection, sql)
        ibm_db.bind_param(stmt, 1, useremail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signup.html', msg="You are already a member, please login using your details")

        else:
            otp = randint(000000, 999999)
            email = request.form['email']
            msg = Message(subject='OTP', sender='hackjacks@gmail.com',
                        recipients=[email])
            msg.body = "You have succesfully registered on hackjacks!\nUse the OTP given below to verify your email ID.\n\t" + \
                str(otp)
            mail.send(msg)
            return render_template('verification.html')

    if request.method == 'GET':
        otp = randint(000000, 999999)
        msg = Message(subject='OTP', sender='hackjacks@gmail.com',
                        recipients=[email])
        msg.body = "You have succesfully registered on hackjacks!\nUse the OTP given below to verify your email ID.\n\t" + \
                str(otp)
        mail.send(msg)
        return render_template('verification.html',msg="OTP has been resent")

@app.route('/validate', methods=['POST'])
def validate():

    user_otp = request.form['otp']
    if otp == int(user_otp):
        insert_sql = "INSERT INTO User VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(connection, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, first_name)
        ibm_db.bind_param(prep_stmt, 2, last_name)
        ibm_db.bind_param(prep_stmt, 3, useremail)
        ibm_db.bind_param(prep_stmt, 4, password)
        ibm_db.execute(prep_stmt)
        return render_template('signin.html')

    else:
        return render_template('verification.html', msg="OTP is invalid. Please enter a valid OTP")

@app.route("/signup")
def signup1():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sql = "SELECT * FROM user WHERE email =?"
        stmt = ibm_db.prepare(connection, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            if (password == None or str(account['PASS']).strip()):
                return render_template('index.html')
            else:
                return render_template('signin.html', msg="Password is invalid")
        else:
            return render_template('signin.html', msg="Email is invalid")
    else:
        return render_template('signin.html')
