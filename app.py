from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from datetime import date

app = Flask(__name__)
app.secret_key = "1234"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://beffe282d753f7:8d0d7099@us-cdbr-east-05.cleardb.net'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired()])
    submit = SubmitField("Login")


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    idnum = db.Column(db.String(20))
    mobnum = db.Column(db.String(20))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    dose = db.Column(db.String(10))
    date = db.Column(db.String(10))
    date1 = db.Column(db.String(10))

    def __init__(self, fname, lname, address, city, idnum, mobnum, age, sex, dose, date, date1):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.idnum = idnum
        self.mobnum = mobnum
        self.age = age
        self.sex = sex
        self.dose = dose
        self.date = date
        self.date1 = date1


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300))
    passwrd = db.Column(db.String(300))
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    pet = db.Column(db.String(200))

    def __init__(self, username, passwrd, firstname, lastname, pet):
        self.username = username
        self.passwrd = passwrd
        self.firstname = firstname
        self.lastname = lastname
        self.pet = pet


@ app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    password = None
    form = LoginForm()
    all_data = Account.query.all()
    listt = []
    for data in all_data:
        newData = []
        newData.append(data.username)
        newData.append(data.passwrd)
        newData.append(data.firstname)
        newData.append(data.lastname)
        listt.append(newData)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        for i in range(len(listt)):
            if username == listt[i][0] and password == listt[i][1]:
                name = f"{listt[i][2]} {listt[i][3]}!"

                flash("Good Day ", name)
                print('success')
                return redirect(url_for('home'))

            elif username != listt[i][0] or password != listt[i][1]:
                l = len(listt) - 1
                if i == l:
                    flash("Wrong Credentials!")
                    return redirect(url_for('index'))

    form.username.data = ""
    form.password.data = ""
    return render_template('login.html',
                           username=username,
                           password=password,
                           form=form)


@ app.route('/home')
def home():
    all_data = Data.query.all()
    today = date.today()
    formatDate = today.strftime("%Y-%m-%d")
    return render_template('index.html', allData=all_data, date=formatDate)


@ app.route('/monitor')
def monitor():
    all_data = Data.query.all()
    return render_template('monitoring.html', allData=all_data)


@ app.route('/about')
def about():
    return render_template('about.html')


@ app.route('/done')
def done():
    all_data = Data.query.all()
    return render_template('done.html', allData=all_data)


@ app.route('/view/<id>/<fname>/<lname>/<sex>/<age>/<dose>/<address>/<city>/<mobnum>')
def view(id, fname, lname, sex, age, dose, address, city, mobnum):
    id = id
    fname = fname
    lname = lname
    sex = sex
    age = age
    dose = dose
    address = address
    city = city
    mobnum = mobnum
    return render_template('view.html', id=id, fname=fname,
                           lname=lname, sex=sex,
                           age=age, dose=dose,
                           address=address, city=city,
                           mobnum=mobnum)


@ app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        city = request.form['city']
        idnum = request.form['idnum']
        mobnum = request.form['mobnum']
        age = request.form['age']
        sex = request.form['sex']
        dose = request.form['dose']

        date = request.form['sched']
        day = date[-2:]
        month = date[5:7]
        yr = date[0:4]
        date1 = f"{day}-{month}-{yr}"
        finalDate = f"{day}-{month}-{yr}"

        my_data = Data(fname, lname, address, city,
                       idnum, mobnum, age, sex, dose, finalDate, date1)
        db.session.add(my_data)
        db.session.commit()

        flash("Resident Info added to the database successfully!")
        return redirect(url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_date = Data.query.get(request.form.get('id'))
        my_date.fname = request.form['fname']
        my_date.lname = request.form['lname']
        my_date.age = request.form['age']
        my_date.sex = request.form['sex']
        my_date.address = request.form['address']
        my_date.city = request.form['city']
        my_date.mobnum = request.form['mobnum']
        my_date.dose = request.form['dose']
        my_date.idnum = request.form['idnum']

        db.session.commit()
        flash("Updated Data Successfully")
        return redirect(url_for('home'))


@app.route('/update1', methods=['GET', 'POST'])
def update1():
    if request.method == 'POST':
        my_date = Data.query.get(request.form.get('id'))
        date = request.form['schedu']
        day = date[-2:]
        month = date[5:7]
        yr = date[0:4]
        finalDate = f"{day}-{month}-{yr}"
        my_date.date = finalDate
        my_date.date1 = finalDate
        db.session.commit()
        flash("Rescheduled Successfully")
        return redirect(url_for('sched'))


@app.route('/update2', methods=['GET', 'POST'])
def update2():
    if request.method == 'POST':
        my_date = Data.query.get(request.form.get('id'))
        date = request.form['schedu']
        day = date[-2:]
        month = date[5:7]
        yr = date[0:4]
        finalDate = f"{day}-{month}-{yr}"
        my_date.date = finalDate
        my_date.date1 = finalDate

        db.session.commit()
        flash("Rescheduled Successfully")
        return redirect(url_for('done'))


@app.route('/doneVaccinated/<id>', methods=['GET', 'POST'])
def doneVaccinated(id):
    my_commit = Data.query.get(id)
    my_commit.date = 'Done'

    db.session.commit()
    return redirect(url_for('sched'))


@app.route('/cancelVaccinated/<id>', methods=['GET', 'POST'])
def cancelVaccinated(id):
    my_commit = Data.query.get(id)
    my_commit.date = 'Cancel'

    db.session.commit()
    return redirect(url_for('sched'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Data successfully deleted!")
    return redirect(url_for('home'))


@app.route('/schedule')
def sched():
    today = date.today()
    formatDate = today.strftime("%d/%m/%Y")
    newFormat = today.strftime("%d-%m-%Y")
    newformatDate = today.strftime("%Y-%m-%d")
    all_data = Data.query.all()
    return render_template('schedule.html', date=formatDate, allData=all_data, newFormat=newFormat, newformatDate=newformatDate)


@app.route('/signupPage')
def signupPage():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        passwrod = request.form['pass']
        fname = request.form['fname']
        lname = request.form['lname']
        confirmpasswrod = request.form['cpass']
        pet = request.form['pet']

        if passwrod != confirmpasswrod:
            flash("Those passwords didn't match. Try again.", "danger")
        else:
            my_data = Account(username, passwrod, fname, lname, pet)
            db.session.add(my_data)
            db.session.commit()
            flash("Successfully Register!", "success")
    return redirect(url_for('signupPage'))


@app.route('/forgot', methods=['POST'])
def forgot():
    all_data = Account.query.all()
    listt = []
    for data in all_data:
        newData = []
        newData.append(data.username)
        newData.append(data.pet)
        newData.append(data.passwrd)
        listt.append(newData)

    if request.method == 'POST':
        u = request.form['uname']
        pet = request.form['pet']
        for i in range(len(listt)):
            if u == listt[i][0] and pet == listt[i][1]:
                passwrd = listt[i][2]
                p = f'Your password is {passwrd}'
                return render_template('showpasswrod.html', p=p)
            elif u == listt[i][0] and pet != listt[i][1]:
                p = f"{u} has no pet '{pet}'"
                return render_template('showpasswrod.html', p=p)
            elif u != listt[i][0]:
                p = f"'{u}' username doesnt exist!"
                return render_template('showpasswrod.html', p=p)

    return redirect(url_for('index'))


@app.route('/chart')
def chart():
    all_data = Data.query.all()
    return render_template('chart.html', allData=all_data)


@app.route('/covidFacts')
def covid():
    return render_template('covid.html')


if __name__ == '__main__':
    app.run(debug=True)
