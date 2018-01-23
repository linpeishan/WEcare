from flask import Flask, render_template, request, flash, redirect, url_for,session
from wtforms import Form, StringField, SelectField, IntegerField, DateTimeField, RadioField, validators, PasswordField, FileField, TextField
from wtforms.fields.html5 import EmailField
#--------------------------------------------------------------
from Doctor import Doctor
from Instructor import Instructor
from Register import Register
from RegisterInstructor import RegisterInstructor
from RegisterDoctor import RegisterDoctor
from Login import Login
from ListOfNamesD import ListOfNamesD

#firebase stuffs
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/booking-b814e-firebase-adminsdk-j8prf-51aedf5eb9.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://booking-b814e.firebaseio.com/'
})
root = db.reference()

app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------------------
#Indicate what's needed for that form; for radio field
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
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#LOGIN AND SIGN UP PAGE
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class LoginForm(Form):
    accountType = RadioField('Account Type', [validators.DataRequired()],
                             choices=[('iuser', 'User'), ('idoctor', 'Doctor'),
                                      ('iinstructor', 'Instructor')], default="iuser")
    username = StringField('Username', [validators.DataRequired('Invalid Username'),validators.length(min=5,max=12)])
    password = PasswordField('Password', [validators.DataRequired('Invalid Password'),validators.length(min=6,max=20)])

#----------------------------------------------------------------------------------------------------------
myUsername = []
myAccountType = []
#----------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    #get username / password
    accountType = form.accountType.data
    username = form.username.data
    password = form.password.data
#CALLING DATABASE OUT AND APPENDING THEM
    accounts = root.child('accounts').get()
    list = []
    for accountid in accounts:
        eachaccount = accounts[accountid]
        account = Login(eachaccount['account type'], eachaccount['username'], eachaccount['password'])
        account.set_registerid(accountid)
        list.append(account)
#---------------------------------------------------------
    if request.method == 'POST' and form.validate():
        accountType_list = []
        username_list = []
        password_list = []
        while True:
            for result in list:
                accountType_list.append(result.get_accountType())
                username_list.append(result.get_username())
                password_list.append(result.get_password())
            print("Account type:",accountType_list)
            print("Username:",username_list)
            print("Password",password_list)
            break
        if username in username_list and password in password_list:
            num = password_list.index(password)
            if username_list.index(username) == password_list.index(password) and accountType_list[num] == accountType :

                print('username:', username_list.index(username))
                print('password:', password_list.index(password))
                print("account:", accountType_list[num])

                myUsername.append(username)
                myAccountType.append(accountType_list[num])

                session['logged_in'] = True
                return redirect(url_for('view_Booking_Page'))

        else:
            error = 'Invalid login'
            flash(error,'danger')
            return render_template('login.html',form=form)
    return render_template('login.html', form=form)
#------------------------------------------------------------
#--------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    myUsername.pop()
    myAccountType.pop()
    return redirect(url_for('login'))
#-----------------------------------------------------------------------------------------------------------------
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
    username = StringField('Username', [validators.DataRequired('Please enter your username'),validators.length(min=5,max=12)])
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
    return render_template('register.html', form=form)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#END OF LOGIN AND SIGN UP PAGE
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------






















































































#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#BOOKING PAGE(*****CONTAINS BOOKING FORM, VIEW BOOKINGS(ABLE TO DELETE AND CHANGE THEM) )
# View Booking Page  AKA VIEW_ALL_PUBLICATIONS.html
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/view_Booking_Page')
def view_Booking_Page():
    bookings = root.child('bookings').get()
    list = [] #store booking objects
    if bookings == None:
        pass
    else:
        for typeid in bookings:
            eachbooking = bookings[typeid]
            print(myAccountType)
            if eachbooking['type'] == 'idoctor':
                doctor = Doctor(eachbooking['name'],eachbooking['age'],
                                eachbooking['phoneNumber'],eachbooking['email'],
                                eachbooking['startingDateAndTime'],eachbooking['type'],eachbooking['created by'],
                                eachbooking['specialization1'])
                doctor.set_typeid(typeid)
                print(doctor.get_typeid())
                if doctor.get_created_by() == myUsername[0] and myAccountType[0] == "iuser":
                    list.append(doctor)
                elif myAccountType[0] == "idoctor":
                    list.append(doctor)
                    return render_template('viewBookingPageDI.html', bookings=list)
            elif eachbooking['type'] == 'iinstructor':
                instructor = Instructor(eachbooking['name'],eachbooking['age'],
                                eachbooking['phoneNumber'],eachbooking['email'],
                                eachbooking['startingDateAndTime'],eachbooking['type'],eachbooking['created by'],
                                eachbooking['specialization2'])
                instructor.set_typeid(typeid)
                print(instructor.get_typeid())
                if instructor.get_created_by() == myUsername[0] and myAccountType[0] == "iuser":
                    list.append(instructor)
                elif myAccountType[0] == "iinstructor":
                    list.append(instructor)
                    return render_template('viewBookingPageDI.html', bookings=list)
    return render_template('viewBookingPage.html',bookings = list)

#------------------------------------------------------------------------
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
            account = ListOfNamesD(eachaccount['account type'],eachaccount['first name'],eachaccount['last name'] ,eachaccount['username'], eachaccount['specialization'])
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
    print(doctorNames)
    print(instructorNames)
    #-------------------------------------------------------------------------------------------------
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
        ins.append((instructorNames["first name"][j] + " " + instructorNames["last name"][j] + " (" + instructorNames["specialization"][j] + ")",instructorNames["first name"][j] + " " + instructorNames["last name"][j] + " (" + instructorNames["specialization"][j] + ")"))

    specialization1 = SelectField("Specialization(Doctors) ", [RequiredIf(type="idoctor")],
                                  choices=doc,
                                  default="")
    specialization2 = SelectField("Specialization(Instructors) ",[RequiredIf(type="iinstructor")],
                                  choices=ins,
                                  default="")
    startingDateAndTime = StringField("Starting Date & Time ", [validators.DataRequired()])
    #---------------------------------------------------------------------------------------------------
    #credit card page
    cardType = RadioField('Payment Details  ',[validators.DataRequired("Please enter your card type")],choices=[('ivisa','Visa'),('imastercard','Master Card'),('iamericanexpress','American Express')],default="ivisa")
    cardName = StringField("Card Name ",[validators.Length(min=1,max=150),validators.DataRequired("Please enter your card name")])
    cardNumber = StringField("Card Number ",[validators.DataRequired("Please enter your card number"),validators.length(min=16,max=16)])
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
                                                                                       ("2017","2017"),
                                                                                       ("2018", "2018"),
                                                                                       ("2019", "2019"),
                                                                                       ("2020", "2020"),
                                                                                       ("2021","2021"),
                                                                                       ("2022","2022"),
                                                                                       ("2023","2023")],
                                                                                        default="")
    cvcode = StringField("Card CV ",[validators.DataRequired("Please enter your CV code"),validators.length(min=3,max=3)])


@app.route('/bookingPage',methods=["GET","POST"]) #@app.route('/newpublication')
def bookingpage():
    form = bookingPage(request.form)
    if request.method == 'POST' and form.validate():
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
            startingDateAndTime = form.startingDateAndTime.data
            type = form.type.data
            created_by = myUsername[0]

            instructor = Instructor(name,age,phoneNumber,email,startingDateAndTime,type,created_by,specialization2)

            book_db = root.child('bookings')
            book_db.push({
                'name' : instructor.get_name(),
                'age' : instructor.get_age(),
                'phoneNumber' : instructor.get_phoneNumber(),
                'email' : instructor.get_email(),
                'startingDateAndTime' : instructor.get_startingDateAndTime(),
                'type' : instructor.get_type(),
                'specialization2' : instructor.get_specialization2(),
                'created by': instructor.get_created_by()
            })

            flash('Your appointment is registered.', 'success')

        return redirect(url_for('view_Booking_Page'))
        # return render_template('view_Booking_Page.html',form=form)
    return render_template('BookingPage.html', form=form)


#update/ change date and time aka update_publications
@app.route('/update/<string:id>/',methods=['GET','POST'])
def update_bookings(id):
    form = bookingPage(request.form)
    if request.method == 'POST' and form.validate():
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
    # return redirect(url_for("view_Booking_Page"))
#cancel appointment
@app.route('/delete_bookings/<string:id>',methods = ['POST'])
def delete_booking(id):
    book_db = root.child('bookings/'+id)
    book_db.delete()
    flash('Appoinment Cancelled','success')

    return redirect(url_for('view_Booking_Page'))


@app.route('/videoChat')
def videoChat():
    return render_template('VideoChat.html')

if __name__ == '__main__':
    app.secret_key = "helloworld"
    app.run()