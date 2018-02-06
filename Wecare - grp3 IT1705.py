from flask import Flask, render_template, request, flash, redirect, url_for,session
from wtforms import Form, StringField, SelectField, IntegerField, RadioField, validators, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateTimeField
#--------------------------------------------------------------
from BookingPage import BookingPage
from Doctor import Doctor
from Instructor import Instructor
from Register import Register
from RegisterInstructor import RegisterInstructor
from RegisterDoctor import RegisterDoctor
from Login import Login
from ListOfNamesD import ListOfNamesD
from datetime import datetime
from Jo_Classes import QueryPage
from Jo_Classes import FitnessArticle
from Jo_Classes import DietaryArticle
from Jo_Classes import EnquiryAnswers
from reviews import Reviews

#firebase stuffs
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/booking-b814e-firebase-adminsdk-j8prf-51aedf5eb9.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://booking-b814e.firebaseio.com/'
})
root = db.reference()

app = Flask(__name__)

class RequiredIf(object):
    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

class LoginForm(Form):
    accountType = RadioField('Account Type', [validators.DataRequired()],
                             choices=[('iuser', 'User'), ('idoctor', 'Doctor'),
                                      ('iinstructor', 'Instructor')], default="iuser")
    username = StringField('Username', [validators.DataRequired('Invalid Username'),validators.length(min=5)])
    password = PasswordField('Password', [validators.DataRequired('Invalid Password'),validators.length(min=6,max=20)])
#-------------------------------------------------------
myUsername = []
myAccountType = []
myName = []
myPassword = []
myFirstNameLastName = []
#-------------------------------------------------------
@app.route('/test')
def test():
    return render_template('test.html')
@app.route('/test1')
def test1():
    return render_template('connection_error_message.html')
@app.route('/home')
def home():
    if not myName:
        session.clear()
    else:
        session['logged_in'] = True
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data
        accounts = root.child('accounts').get()
        list = []
        dlist = []
        ilist = []
        dNames = {"first name":[],"last name":[],"specialization":[],"username":[]}
        dcount = []
        iNames = {"first name": [], "last name": [], "specialization": [], "username": []}
        icount = []
        for accountid in accounts:
            eachaccount = accounts[accountid]
            account = Login(eachaccount['account type'], eachaccount['username'], eachaccount['password'], eachaccount['first name'], eachaccount['last name'])
            account.set_registerid(accountid)
            list.append(account)

            if account.get_accountType() == "idoctor":
                account =   ListOfNamesD(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],eachaccount['username'],
                                         eachaccount['specialization'])
                dNames["first name"].append(account.get_firstName())
                dNames["last name"].append(account.get_lastName())
                dNames["specialization"].append(account.get_specialization())
                dcount.append(account.get_username())

            elif account.get_accountType() == "iinstructor":
                account =   ListOfNamesD(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],eachaccount['username'],
                                         eachaccount['specialization'])
                iNames["first name"].append(account.get_firstName())
                iNames["last name"].append(account.get_lastName())
                iNames["specialization"].append(account.get_specialization())
                icount.append(account.get_username())

        for i in range(len(dcount)):
            dlist.append(dNames["first name"][i] + " " + dNames["last name"][i] + " (" +
                        dNames["specialization"][i] + ")")
        for i in range(len(icount)):
            ilist.append(iNames["first name"][i] + " " + iNames["last name"][i] + " (" +
                        iNames["specialization"][i] + ")")
        if not myName:
            session.clear()
        else:
            session['logged_in'] = True
            return redirect('/home')
        if request.method == 'POST' and form.validate():
            accountType_list = []
            username_list = []
            password_list = []
            name_list = []
            while True:
                for result in list:
                    accountType_list.append(result.get_accountType())
                    username_list.append(result.get_username())
                    password_list.append(result.get_password())
                    name_list.append(result.get_firstName()+" "+result.get_lastName())
                break

            if username in username_list and password in password_list:
                num = password_list.index(password)
                yo = []
                if username_list.index(username) == password_list.index(password):
                    if accountType_list[num] == "idoctor":
                        for i in range(len(dcount)):
                            if username == dcount[i]:
                                yo.append(i)

                        myName.append(dlist[yo[0]])
                    elif accountType_list[num] == "iinstructor":
                        for i in range(len(icount)):
                            if username == icount[i]:
                                yo.append(i)

                        myName.append(ilist[yo[0]])
                    else:
                        myName.append(None)

                    myUsername.append(username)
                    myAccountType.append(accountType_list[num])
                    myPassword.append(password)
                    myFirstNameLastName.append(name_list[num])
                    session['logged_in'] = True
                    return redirect(url_for('home'))

            else:
                error = 'Invalid login'
                flash(error,'danger')
                return render_template('login.html',form=form)
    except:
        render_template("error_message.html")
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    try:
        session.clear()
        myUsername.pop()
        myAccountType.pop()
        myName.pop()
        myPassword.pop()
        myFirstNameLastName.pop()

    except IndexError:
        return render_template("logout_error.html")
    else:
        flash('You are now logged out', 'success')
        return redirect(url_for('login'))

class signup(Form):
    accountType = RadioField('Account Type', [validators.DataRequired()],
                          choices=[('iuser', 'User'), ('idoctor', 'Doctor'),
                                   ('iinstructor', 'Instructor')], default="iuser")
    gender = SelectField("Gender ", [validators.DataRequired("Please select your gender")], choices=[("", "Please Select:"),
                                                                          ("Female", "Female"),
                                                                          ("Male", "Male"),
                                                                          ("It\'s complicated", "It\'s complicated"),
                                                                          ("Rather not say", "Rather not say"),
                                                                          ],
                                                                          default="")
    first_name = StringField('First Name', [validators.DataRequired('Please enter your first name')])
    last_name = StringField('Last Name', [validators.DataRequired('Please enter your last name')])
    username = StringField('Username', [validators.DataRequired('Please enter your username'),validators.length(min=5)])
    email = EmailField("Email ", [validators.DataRequired("Email address is required"),
                                  validators.Email('Please enter your email')])
    password = PasswordField('Password', [validators.DataRequired('Password is required.'),validators.Length(min=6,max=20)])
    phoneNumber = StringField('Contact Number', [validators.DataRequired('Please enter your phone number'),validators.length(min=8,max=8)])
    age = IntegerField('Age', [validators.DataRequired('Age is range from 1 to 200 only'),
                               validators.number_range(min=1, max=200)])
    specialization1 = SelectField("Specialization(Doctors)", [RequiredIf(accountType="idoctor")],
                                  choices=[("", "Please Select"),
                                           ("Anesthesiologist", "Anesthesiologist"),
                                           ("Allergist", "Allergist"),
                                           ("Audiologist", "Audiologist"),
                                           ("Cardiologist", "Cardiologist"),
                                           ("Dentist", "Dentist"), ],
                                  default="")

    specialization2 = SelectField("Specialization(Instructors) ", [RequiredIf(accountType="iinstructor")],
                                  choices=[("", "Please Select:"),
                                           ("Yoga", "Yoga"),
                                           ("Zumba", "Zumba"),
                                           ("Kardio", "Kardio"),
                                           ("Kickbox", "Kickbox"),
                                           ("Dance", "Dance"),
                                           ],
                                  default="")


@app.route('/signup',methods=["GET","POST"])
def register():
    try:
        form = signup(request.form)
        if request.method == 'POST' and form.validate():
            if form.accountType.data == "iuser":
                accountType = form.accountType.data
                firstName = form.first_name.data
                lastName = form.last_name.data
                username = form.username.data
                password = form.password.data
                age = form.age.data
                gender = form.gender.data
                email = form.email.data
                contactNumber = form.phoneNumber.data

                user = Register(accountType,firstName,lastName,username,password,age,gender,email,contactNumber)

                user_db = root.child('accounts')
                user_db.push({
                    'account type':user.get_accountType(),
                    'first name':user.get_firstName(),
                    'last name': user.get_lastName(),
                    'username': user.get_username(),
                    'password':user.get_password(),
                    'age':user.get_age(),
                    'gender':user.get_gender(),
                    'email': user.get_email(),
                    'contact number': user.get_contactNumber()
                })

                flash("Your USER account is registered successfully! Your username is now "+user.get_username(),"success")

            elif form.accountType.data == "idoctor":
                accountType = form.accountType.data
                firstName = form.first_name.data
                lastName = form.last_name.data
                username = form.username.data
                password = form.password.data
                age = form.age.data
                gender = form.gender.data
                email = form.email.data
                contactNumber = form.phoneNumber.data
                specialization1 = form.specialization1.data

                userDoctor = RegisterDoctor(accountType, firstName, lastName, username, password, age, gender, email, contactNumber,specialization1)

                user_db = root.child('accounts')
                user_db.push({
                    'account type': userDoctor.get_accountType(),
                    'first name': userDoctor.get_firstName(),
                    'last name': userDoctor.get_lastName(),
                    'username': userDoctor.get_username(),
                    'password': userDoctor.get_password(),
                    'age': userDoctor.get_age(),
                    'gender': userDoctor.get_gender(),
                    'email': userDoctor.get_email(),
                    'contact number': userDoctor.get_contactNumber(),
                    'specialization' : userDoctor.get_specialization1()
                })

                flash("Your DOCTOR account is registered successfully! Your username is now "+userDoctor.get_username(), "success")
            elif form.accountType.data == "iinstructor":
                accountType = form.accountType.data
                firstName = form.first_name.data
                lastName = form.last_name.data
                username = form.username.data
                password = form.password.data
                age = form.age.data
                gender = form.gender.data
                email = form.email.data
                contactNumber = form.phoneNumber.data
                specialization2 = form.specialization2.data

                userInstructor = RegisterInstructor(accountType, firstName, lastName, username, password, age, gender, email, contactNumber,specialization2)

                user_db = root.child('accounts')
                user_db.push({
                    'account type': userInstructor.get_accountType(),
                    'first name': userInstructor.get_firstName(),
                    'last name': userInstructor.get_lastName(),
                    'username': userInstructor.get_username(),
                    'password': userInstructor.get_password(),
                    'age': userInstructor.get_age(),
                    'gender': userInstructor.get_gender(),
                    'email': userInstructor.get_email(),
                    'contact number': userInstructor.get_contactNumber(),
                    'specialization' : userInstructor.get_specialization2()
                })

                "Your INSTRUCTOR account is registered successfully! Your username is now " + userInstructor.get_username()
            return redirect(url_for('login'))

    except:
        render_template("error_message.html")
    else:
        return render_template('register.html', form=form)

@app.route('/view_Booking_Page')
def view_Booking_Page():
    try:
        if not myName:
            return redirect("/login")
        else:
            bookings = root.child('bookings').get()
            list = []  # store booking objects
            if bookings == None:
                pass
            else:
                for typeid in bookings:
                    eachbooking = bookings[typeid]
                    if eachbooking['type'] == 'idoctor':
                        doctor = Doctor(eachbooking['name'],eachbooking['age'],
                                        eachbooking['phoneNumber'],eachbooking['email'],
                                        eachbooking['startingDateAndTime'],eachbooking['type'],eachbooking['created by'],
                                        eachbooking['specialization1'])
                        doctor.set_typeid(typeid)
                        if doctor.get_created_by() == myUsername[0] and myAccountType[0] == "iuser":
                            list.append(doctor)
                        elif myAccountType[0] == "idoctor":
                            if doctor.get_specialization1() == myName[0]:
                                list.append(doctor)
                    elif eachbooking['type'] == 'iinstructor':
                        instructor = Instructor(eachbooking['name'],eachbooking['age'],
                                        eachbooking['phoneNumber'],eachbooking['email'],
                                        eachbooking['startingDateAndTime'],eachbooking['type'],eachbooking['created by'],
                                        eachbooking['specialization2'])
                        instructor.set_typeid(typeid)
                        if instructor.get_created_by() == myUsername[0] and myAccountType[0] == "iuser":
                            list.append(instructor)
                        elif myAccountType[0] == "iinstructor":
                            if instructor.get_specialization2() == myName[0]:
                                list.append(instructor)
            if myAccountType[0] == "iuser":
                return render_template('viewBookingPage.html',bookings = list)
            else:
                return render_template('viewBookingPageDI.html',bookings = list)
    except:
        render_template("error_message.html")
dcount = []
icount = []
doctorNames = {"first name":[],"last name":[],"username":[],"specialization":[]}
instructorNames = {"first name":[],"last name":[],"username":[],"specialization":[]}

class bookingPage(Form):#aka class PublicationForm(Form)
    accounts = root.child('accounts').get()
    for accountid in accounts:
        eachaccount = accounts[accountid]
        account = ListOfNamesD(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                               eachaccount['username'], eachaccount['password'])
        if account.get_accountType() == "idoctor":
            account = ListOfNamesD(eachaccount['account type'],eachaccount['first name'],eachaccount['last name'] ,eachaccount['username'],
                                   eachaccount['specialization'])
            doctorNames["username"].append(account.get_username())
            doctorNames["first name"].append(account.get_firstName())
            doctorNames["last name"].append(account.get_lastName())
            doctorNames["specialization"].append(account.get_specialization())
            dcount.append(account.get_username())
        elif account.get_accountType() == "iinstructor":
            account = ListOfNamesD(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                                   eachaccount['username'], eachaccount['specialization'])
            instructorNames["username"].append(account.get_username())
            instructorNames["first name"].append(account.get_firstName())
            instructorNames["last name"].append(account.get_lastName())
            instructorNames["specialization"].append(account.get_specialization())
            icount.append(account.get_username())
    type = RadioField('Choose type  ',[validators.DataRequired("Please choose one")],choices=[('idoctor','Doctor'),('iinstructor','Instructor')],default="idoctor")
    name = StringField("Name (Mr/Ms/Madam) ",[validators.Length(min=1,max=150),validators.DataRequired("Please enter your name")])
    age = IntegerField("Age ",[validators.DataRequired("Please enter your age")])
    phoneNumber = StringField("Number ",[validators.DataRequired("Please enter your contact number"),validators.length(min=8,max=8)]) #kiv,will validate to sg number format
    email = EmailField("Email ", [validators.DataRequired("Please enter your email"), validators.Email()])
    doc = [("", "---")]
    ins = [("", "---")]
    for i in range(len(dcount)):
        doc.append((doctorNames["first name"][i] + " " + doctorNames["last name"][i] + " (" +doctorNames["specialization"][i] + ")" , doctorNames["first name"][i] + " " + doctorNames["last name"][i] + " (" +doctorNames["specialization"][i] + ")"))
    for j in range(len(icount)):
        ins.append((instructorNames["first name"][j] + " " + instructorNames["last name"][j] + " (" + instructorNames["specialization"][j] + ")" ,instructorNames["first name"][j] + " " + instructorNames["last name"][j] + " (" + instructorNames["specialization"][j] + ")"))

    specialization1 = SelectField("Specialization(Doctors) ", [RequiredIf(type="idoctor")],
                                  choices=doc,
                                  default="")
    specialization2 = SelectField("Specialization(Instructors) ",[RequiredIf(type="iinstructor")],
                                  choices=ins,
                                  default="")

    # startingDateAndTime = DateTimeField("Starting Date & Time ", [validators.DataRequired()],
    #                      format="%d %B %Y %I:%M%p",default=datetime.now)

    startingDateAndTime = StringField("Starting Date & Time ", [validators.DataRequired()],
                                      default=datetime.today().strftime('%d %B %Y %I:%M%p'))
    #---------------------------------------------------------------------------------------------------
    #credit card page
    cardType = RadioField('Payment Details  ',[validators.DataRequired("Please enter your card type")],choices=[('ivisa','Visa'),('imastercard','Master Card'),('iamex','Amex')],default="ivisa")
    cardName = StringField("Card Name ",[validators.Length(min=1,max=150),validators.DataRequired("Please enter your card name")])
    cardNumber = StringField("Card Number ",[validators.DataRequired("Please enter your card number")])
    expirationMonth = SelectField("Expiration Date ",[validators.DataRequired("Please enter the expiry month")],choices=[("","Please Select:"),
                                                                                       ("January","January"),
                                                                                       ("February", "Febuary"),
                                                                                       ("March", "March"),
                                                                                       ("April", "April"),
                                                                                       ("May","May"),
                                                                                       ("June","June"),
                                                                                       ("July","July"),
                                                                                       ("August","August"),
                                                                                       ("September","September"),
                                                                                       ("October","October"),
                                                                                       ("November","November"),
                                                                                       ("December","December")],
                                                                                        default="")
    expirationYear = SelectField("Expiration Year ",[validators.DataRequired("Please enter the expiry year")],choices=[("","Please Select:"),
                                                                                       ("2018", "2018"),
                                                                                       ("2019", "2019"),
                                                                                       ("2020", "2020"),
                                                                                       ("2021","2021"),
                                                                                       ("2022","2022"),
                                                                                       ("2023","2023")],
                                                                                        default="")
    cvcode = StringField("Card CV ",[validators.DataRequired("Please enter your CV code"),validators.length(min=3,max=3)])


@app.route('/bookingPage',methods=["GET","POST"])
def bookingpage():
    try:
        if not myName:
            return redirect("/login")
        else:
            try:
                if myAccountType[0] == "iuser":
                    bookings = root.child('bookings').get()
                    list = []  # store date and time
                    for typeid in bookings:

                        eachbooking = bookings[typeid]
                        info = BookingPage(eachbooking['name'], eachbooking['age'],
                                            eachbooking['phoneNumber'], eachbooking['email'],
                                            eachbooking['startingDateAndTime'], eachbooking['type'],
                                            eachbooking['created by'])
                        list.append(info.get_startingDateAndTime())
                    #----------------------------------
                    form = bookingPage(request.form)

                    if request.method == 'POST' and form.validate():
                        #---------------------------------------------------
                        if form.cardType.data == "ivisa":
                            if len(form.cardNumber.data) == 16:
                                if int(form.cardNumber.data[0]) == 4:
                                    flash("Visa's number approved!", "success")
                            else:
                                flash("Invalid card number", "danger")
                                return redirect("/bookingPage")
                        elif form.cardType.data == "iamex":
                            if len(form.cardNumber.data) == 15:
                                if int(form.cardNumber.data[0:2]) > 33 and int(form.cardNumber.data[0:2]) < 38:
                                    flash("Amex's number approved!", "success")
                            else:
                                flash("Invalid card number", "danger")
                                return redirect("/bookingPage")
                        elif form.cardType.data == "imastercard":
                            if len(form.cardNumber.data) == 16:
                                if int(form.cardNumber.data[0:2]) > 50 and int(form.cardNumber.data[0:2]) < 56:
                                    flash("MasterCard's number approved", "success")
                            else:
                                flash("Invalid card number", "danger")
                                return redirect("/bookingPage")
                    #-------------------------------------------------
                        if form.type.data == "idoctor":
                            name = form.name.data
                            age = form.age.data
                            phoneNumber = form.phoneNumber.data
                            email = form.email.data
                            specialization1 = form.specialization1.data
                            type = form.type.data
                            created_by = myUsername[0]
                            startingDateAndTime = form.startingDateAndTime.data
                            for dt in list:
                                # print("dt",dt)

                                if str(form.startingDateAndTime.data) == dt:
                                    flash("Your booking time is invalid","danger")
                                    return redirect("/bookingPage")
                            # startingDateAndTime = str(form.startingDateAndTime.data)
                            if form.cardType.data == "ivisa":
                                if len(form.cardNumber.data) == 16:
                                    if int(form.cardNumber.data[0]) == 4:
                                        flash("Visa's number approved!", "success")
                                else:
                                    flash("Invalid card number", "danger")
                                    return redirect("/bookingPage")
                            elif form.cardType.data == "iamex":
                                if len(form.cardNumber.data) == 15:
                                    if int(form.cardNumber.data[0:2]) > 33 and int(form.cardNumber.data[0:2]) < 38:
                                        flash("Amex's number approved!", "success")
                                else:
                                    flash("Invalid card number", "danger")
                                    return redirect("/bookingPage")
                            elif form.cardType.data == "imastercard":
                                if len(form.cardNumber.data) == 16:
                                    if int(form.cardNumber.data[0:2]) > 50 and int(form.cardNumber.data[0:2]) < 56:
                                        flash("MasterCard's number approved", "success")
                                else:
                                    flash("Invalid card number", "danger")
                                    return redirect("/bookingPage")

                            #-----------------------------------------------------------------------------------------------
                            doctor = Doctor(name,age,phoneNumber,email,startingDateAndTime,type,created_by,specialization1)

                            book_db = root.child('bookings')

                            book_db.push({
                                'name': doctor.get_name(),
                                'age': doctor.get_age(),
                                'phoneNumber': doctor.get_phoneNumber(),
                                'email': doctor.get_email(),
                                'startingDateAndTime': doctor.get_startingDateAndTime(),
                                'type': doctor.get_type(),
                                'specialization1': doctor.get_specialization1(),
                                'created by': doctor.get_created_by()
                            })
                            flash("Your appointment is registered.", 'success')

                        elif form.type.data == "iinstructor":
                            name = form.name.data
                            age = form.age.data
                            phoneNumber = form.phoneNumber.data
                            email = form.email.data
                            specialization2 = form.specialization2.data

                            type = form.type.data
                            created_by = myUsername[0]
                            startingDateAndTime = form.startingDateAndTime.data
                            for dt in list:
                                if dt == form.startingDateAndTime.data:
                                    flash("Time slot has been booked by someone.", "danger")
                                    return redirect("/bookingPage")
                            # startingDateAndTime = str(form.startingDateAndTime.data)
                            instructor = Instructor(name, age, phoneNumber, email, startingDateAndTime, type, created_by,
                                        specialization2)

                            book_db = root.child('bookings')
                            book_db.push({
                                'name': instructor.get_name(),
                                'age': instructor.get_age(),
                                'phoneNumber': instructor.get_phoneNumber(),
                                'email': instructor.get_email(),
                                'startingDateAndTime': instructor.get_startingDateAndTime(),
                                'type': instructor.get_type(),
                                'specialization2': instructor.get_specialization2(),
                                'created by': instructor.get_created_by()
                            })

                            flash('Your appointment is registered.', 'success')

                        return redirect(url_for('view_Booking_Page'))
                    return render_template('BookingPage.html', form=form)
                elif myAccountType[0] == "idoctor" or myAccountType[0] == "iinstructor":
                    return render_template("booking_page_error.html")
            except:
                render_template("error_message.html")
    except:
        render_template("error_message.html")

@app.route('/update/<string:id>/',methods=['GET','POST'])
def update_bookings(id):
    try:
        form = bookingPage(request.form)
        if request.method == 'POST' and form.validate():
            #---------------------------------------------------
            if form.cardType.data == "ivisa":
                if len(form.cardNumber.data) == 16:
                    if int(form.cardNumber.data[0]) == 4:
                        flash("Visa's number approved!", "success")
                else:
                    flash("Invalid card number", "danger")
                    return redirect("/bookingPage")
            elif form.cardType.data == "iamex":
                if len(form.cardNumber.data) == 15:
                    if int(form.cardNumber.data[0:2]) > 33 and int(form.cardNumber.data[0:2]) < 38:
                        flash("Amex's number approved!", "success")
                else:
                    flash("Invalid card number", "danger")
                    return redirect("/bookingPage")
            elif form.cardType.data == "imastercard":
                if len(form.cardNumber.data) == 16:
                    if int(form.cardNumber.data[0:2]) > 50 and int(form.cardNumber.data[0:2]) < 56:
                        flash("MasterCard's number approved", "success")
                else:
                    flash("Invalid card number", "danger")
                    return redirect("/bookingPage")
        #-------------------------------------------------
            if form.type.data == "idoctor":
                name = form.name.data
                age = form.age.data
                phoneNumber = form.phoneNumber.data
                email = form.email.data
                specialization1 = form.specialization1.data
                startingDateAndTime = form.startingDateAndTime.data
                type = form.type.data
                created_by = myUsername[0]

                doctor = Doctor(name,age,phoneNumber,email,startingDateAndTime,type,created_by,specialization1)

                book_db = root.child('bookings/'+id)

                book_db.set({
                    'name': doctor.get_name(),
                    'age': doctor.get_age(),
                    'phoneNumber': doctor.get_phoneNumber(),
                    'email': doctor.get_email(),
                    'startingDateAndTime': doctor.get_startingDateAndTime(),
                    'type': doctor.get_type(),
                    'specialization1': doctor.get_specialization1(),
                    'created by': doctor.get_created_by()
                })

                flash("Your appointment has been rescheduled", 'success')

            else:
                name = form.name.data
                age = form.age.data
                phoneNumber = form.phoneNumber.data
                email = form.email.data
                specialization2 = form.specialization2.data
                startingDateAndTime = form.startingDateAndTime.data
                type = form.type.data
                created_by = myUsername[0]

                instructor = Instructor(name,age,phoneNumber,email,startingDateAndTime,type,created_by,specialization2)

                book_db = root.child('bookings/'+id)

                book_db.set({
                    'name' : instructor.get_name(),
                    'age' : instructor.get_age(),
                    'phoneNumber' : instructor.get_phoneNumber(),
                    'email' : instructor.get_email(),
                    'startingDateAndTime' : instructor.get_startingDateAndTime(),
                    'type' : instructor.get_type(),
                    'specialization2' : instructor.get_specialization2(),
                    'created by': instructor.get_created_by()
                })

                flash('Your appointment has been rescheduled.', 'success')

            return redirect(url_for('view_Booking_Page'))
        else:
            url = 'bookings/' + id
            eachbook = root.child(url).get()

            if eachbook['type'] == 'idoctor':
                doctor = Doctor(eachbook['name'],eachbook['age'],
                                eachbook['phoneNumber'],eachbook['email'],
                                eachbook['startingDateAndTime'],eachbook['type'],eachbook['created by'],
                                eachbook['specialization1'])
                doctor.set_typeid(id)
                form.name.data = doctor.get_name()
                form.age.data = doctor.get_age()
                form.phoneNumber.data = doctor.get_phoneNumber()
                form.email.data = doctor.get_email()
                form.specialization1.data = doctor.get_specialization1()
                form.startingDateAndTime.data = doctor.get_startingDateAndTime()
                form.type.data = doctor.get_type()

            else:
                instructor = Instructor(eachbook['name'], eachbook['age'],
                                        eachbook['phoneNumber'], eachbook['email'],
                                        eachbook['startingDateAndTime'], eachbook['type'],eachbook['created by'],
                                        eachbook['specialization2'])
                instructor.set_typeid(id)
                form.name.data = instructor.get_name()
                form.age.data = instructor.get_age()
                form.phoneNumber.data = instructor.get_phoneNumber()
                form.email.data = instructor.get_email()
                form.specialization2.data = instructor.get_specialization2()
                form.startingDateAndTime.data = instructor.get_startingDateAndTime()
                form.type.data = instructor.get_type()
            return render_template('updateBookingPage.html',form=form)
    except:
        render_template("error_message.html")

#cancel appointment
@app.route('/delete_bookings/<string:id>',methods = ['POST'])
def delete_booking(id):
    try:
        book_db = root.child('bookings/'+id)
        book_db.delete()
        flash('Appoinment Cancelled','success')
    except:
        render_template("error_message.html")
    else:
        return redirect(url_for('view_Booking_Page'))

@app.route('/complete_booking/<string:id>',methods= ['POST'])
def complete_booking(id):
    try:
        book_db = root.child('bookings/'+id)
        book_db.delete()
    except:
        render_template("error_message.html")
    else:
        return redirect(url_for('videoChat'))

@app.route('/videoChat')
def videoChat():
    try:
        if not myName:
            return redirect("/login")
        else:
            if myAccountType[0] == "iuser":
                return render_template('VideoChat.html')
            elif myAccountType[0] == "iinstructor" or myAccountType[0] == "idoctor":
                return render_template('videoChatDI.html')
    except:
        return render_template('error_message.html')

class newArticle(Form):
    title = StringField("Title", [validators.DataRequired()])
    content = TextAreaField("Content", [validators.DataRequired()])
    type_choices = [('Diet', 'Dietary'), ('Fit', 'Fitness')]
    type = RadioField('Type', choices=type_choices, default='Diet')

@app.route('/new-article', methods=['GET', 'POST'])
def new():
    try:
        form = newArticle(request.form)
        if request.method == 'POST' and form.validate():
            if form.type.data == 'Diet':
                title = form.title.data
                content = form.content.data
                type = form.type.data
                dietarticle = DietaryArticle(title, content, type)
                dietarticle_sent = root.child('dietary articles')
                dietarticle_sent.push({
                    'title': dietarticle.get_title(),
                    'content': dietarticle.get_content(),
                    'type': dietarticle.get_type()
                })
                flash('Article Published Successfully', 'success')

            else:
                title = form.title.data
                content = form.content.data
                type = form.type.data
                fitarticle = FitnessArticle(title, content, type)
                fitarticle_sent = root.child('fitness articles')
                fitarticle_sent.push({
                    'title': fitarticle.get_title(),
                    'content': fitarticle.get_content(),
                    'type': fitarticle.get_type()
                })
                flash('Article Published Successfully', 'success')

            return render_template('home.html', form=form)

        if myUsername[0] == "admin" and myPassword[0] == "P@ssw0rd":
            return render_template("Tips_Pages/new_article.html", form=form)

    except IndexError:
        return render_template("new_article_error.html")
    else:
        return render_template("error_message.html")

class queryPage(Form):
    query = TextAreaField("Enquiry", [validators.DataRequired()])

@app.route('/enquiry', methods=['GET', 'POST'])
def query():
    if not myName:
        return redirect("/login")
    else:
        form = queryPage(request.form)
        if request.method == 'POST' and form.validate():
            now = datetime.today().strftime('%d %B %Y %I:%M%p')
            query = form.query.data
            created_by = myUsername[0]
            newquery = QueryPage(query, now, created_by)
            newquery_sent = root.child('queries')
            newquery_sent.push({
                'query': newquery.get_query(),
                'date_time': newquery.get_date_time(),
                'created_by': newquery.get_created_by()
            })
            flash('Enquiry Submitted Sucessfully.', 'success')

            return render_template('home.html', form=form)
        return render_template('enquiry.html', form=form)

@app.route('/enquirylist')
def enquirylist():
    if not myName:
        return redirect("/login")
    else:
        if myAccountType[0] == "idoctor":
            enquiries = root.child('queries').get()
            list = []
            for enquiryid in enquiries:
                eachenquiry = enquiries[enquiryid]
                enquiry1 = QueryPage(eachenquiry['query'], eachenquiry['date_time'], eachenquiry['created_by'])
                enquiry1.set_enquiryid(enquiryid)
                list.append(enquiry1)
            return render_template('enquirylist.html', enquiries=list)
        else:
            return redirect("/home")

class answerPage(Form):
    answer = TextAreaField("Answer", [validators.DataRequired()])

@app.route('/answerEnquiry/<string:id>/', methods=['GET', 'POST'])
def answer(id):
    form = answerPage(request.form)
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        doctorName = myFirstNameLastName[0]
        newanswer = EnquiryAnswers(answer, enquiryid=id, doctorName=doctorName)
        newanswer_sent = root.child('enquiry answers')
        newanswer_sent.push({
            'answer': newanswer.get_answer(),
            'enquiryid': newanswer.get_enquiryid(),
            'doctorName': newanswer.get_doctorName(),
        })
        flash('Answer Sent Sucessfully.', 'success')

        return redirect('/enquirylist')
    return render_template('answerEnquiry.html', form=form)

@app.route('/enquirylistPB')
def enquiryPB():

    answers = root.child('enquiry answers').get()
    answerlist = []

    for answerid in answers:
        eachanswer = answers[answerid]
        answer1 = EnquiryAnswers(eachanswer['answer'], eachanswer['enquiryid'], eachanswer['doctorName'])
        answer1.set_answerid(answerid)
        answerlist.append(answer1)

    enquiries = root.child('queries').get()
    enquirylist = []

    for enquiryid in enquiries:
        eachenquiry = enquiries[enquiryid]
        enquiry1 = QueryPage(eachenquiry['query'], eachenquiry['date_time'], eachenquiry['created_by'])
        enquiry1.set_enquiryid(enquiryid)
        enquirylist.append(enquiry1)

    return render_template('enquirylistPB.html', answers=answerlist, enquiries=enquirylist)

@app.route('/dietary-tip1')
def dietarytip1():
    articles = root.child('dietary articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = DietaryArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/dietarytip1.html', articles = list)

@app.route('/dietary-tip2')
def dietarytip2():
    articles = root.child('dietary articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = DietaryArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/dietarytip2.html', articles = list)

@app.route('/dietary-tip3')
def dietarytip3():
    articles = root.child('dietary articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = DietaryArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/dietarytip3.html', articles = list)

@app.route('/fitness-tip1')
def fitnesstip1():
    articles = root.child('fitness articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = FitnessArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/fitnesstip1.html', articles=list)

@app.route('/fitness-tip2')
def fitnesstip2():
    articles = root.child('fitness articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = FitnessArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/fitnesstip2.html', articles=list)

@app.route('/fitness-tip3')
def fitnesstip3():
    articles = root.child('fitness articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = FitnessArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/fitnesstip3.html', articles=list)

@app.route('/tips-dietary')
def tipsdietary():
    articles = root.child('dietary articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = DietaryArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)
    return render_template('Tips_Pages/healthtips_dietary.html', articles=list)

@app.route('/tips-fitness')
def tipsfitness():
    articles = root.child('fitness articles').get()
    list = []
    for articleid in articles:
        eacharticle = articles[articleid]
        article1 = FitnessArticle(eacharticle['title'], eacharticle['content'], eacharticle['type'])
        article1.set_articleid(articleid)
        list.append(article1)

    return render_template('Tips_Pages/healthtips_fitness.html', articles=list)

@app.route('/doctor')
def doctor():
    accounts = root.child('accounts').get()
    list = []

    for accountid in accounts:
        eachaccount = accounts[accountid]
        account = Register(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                           eachaccount['username'], eachaccount['password'], eachaccount['age'],
                           eachaccount['gender'],eachaccount['email'],
                           eachaccount['contact number'])

        if account.get_accountType() == "idoctor":
            doctor = RegisterDoctor(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                           eachaccount['username'], eachaccount['password'], eachaccount['age'],
                           eachaccount['gender'],eachaccount['email'],
                           eachaccount['contact number'],eachaccount['specialization'])

            list.append(doctor)
            print(doctor.get_username())

    return render_template('doctor.html', accounts=list)

@app.route('/instructor')
def instructor():
    accounts = root.child('accounts').get()
    list = []

    for accountid in accounts:
        eachaccount = accounts[accountid]
        account = Register(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                           eachaccount['username'], eachaccount['password'], eachaccount['age'],
                           eachaccount['gender'],eachaccount['email'],
                           eachaccount['contact number'])

        if account.get_accountType() == "iinstructor":
            instructor = RegisterInstructor(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                           eachaccount['username'], eachaccount['password'], eachaccount['age'],
                           eachaccount['gender'],eachaccount['email'],
                           eachaccount['contact number'],eachaccount['specialization'])

            list.append(instructor)
            print(instructor.get_username())

    return render_template('instructor.html', accounts=list)

class ReviewForm(Form):
    message = TextAreaField('Reviews:', [validators.DataRequired('Please write your review')])


@app.route('/review1', methods=['GET', 'POST'])
def review():
    if not myName:
        return redirect("/login")

    else:
        form = ReviewForm(request.form)
        if request.method == "POST" and form.validate():
            message = form.message.data
            now = datetime.today().strftime('%d %B %Y %I:%M%p')
            created_by = myUsername[0]
            user = Reviews(message, now, created_by)
            user_db = root.child('reviews') #create the thing to firebase
            user_db.push({
                'message': user.get_message(),
                'datetime': user.get_datetime(),
                'created_by': user.get_created_by()
                          })
            flash("Done","success")
            return redirect("/viewReviews")
            # return url_for('/viewReviews',form=form)
            # return render_template('viewReviews.html')
        return render_template('review1.html', form=form)

@app.route('/viewReviews')
def viewReviews():
    reviews = root.child('reviews').get()
    list = [] #store reviews object

    for typeid in reviews:
        eachreview = reviews[typeid]
        m = Reviews(eachreview['message'], eachreview['datetime'], eachreview['created_by'])
        m.set_typeid(typeid)
        list.append(m)
    # print(list)
    return render_template('viewReviews.html', reviews=list)

@app.route('/profilePage')
def profilePage():
    if not myName:
        return redirect("/login")
    else:
        accounts = root.child('accounts').get()
        list = []
        display = []
        for accountid in accounts:
            eachaccount = accounts[accountid]
            account = Register(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                               eachaccount['username'], eachaccount['password'], eachaccount['age'],
                               eachaccount['gender'],eachaccount['email'],
                               eachaccount['contact number'])

            if account.get_accountType() == "iinstructor":
                instructor = RegisterInstructor(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                               eachaccount['username'], eachaccount['password'], eachaccount['age'],
                               eachaccount['gender'],eachaccount['email'],
                               eachaccount['contact number'],eachaccount['specialization'])
                list.append(instructor)
            elif account.get_accountType() == "idoctor":
                doctor = RegisterDoctor(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                               eachaccount['username'], eachaccount['password'], eachaccount['age'],
                               eachaccount['gender'],eachaccount['email'],
                               eachaccount['contact number'],eachaccount['specialization'])

                list.append(doctor)
            elif account.get_accountType() == "iuser":
                user = Register(eachaccount['account type'], eachaccount['first name'], eachaccount['last name'],
                                   eachaccount['username'], eachaccount['password'], eachaccount['age'],
                                   eachaccount['gender'], eachaccount['email'],
                                   eachaccount['contact number'])
                list.append(user)
#---------------------------------------------------------------------------------------------------------------
        for i in list:
            if myUsername[0] == i.get_username():
                display.append(i)
    return render_template('profilePage.html', Register=display)

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.secret_key = "helloworld"
    app.run()