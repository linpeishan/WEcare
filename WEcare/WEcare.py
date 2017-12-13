from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextField, SelectField, IntegerField, DateTimeField, RadioField, validators
from wtforms.fields.html5 import EmailField
from Doctor import Doctor
from Instructor import Instructor


#firebase for booking page
#----start----
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/booking-b814e-firebase-adminsdk-j8prf-51aedf5eb9.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://booking-b814e.firebaseio.com/'
})
root = db.reference()
#----end-----

app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/videoChat')
def videoChat():
    return render_template('VideoChat.html')
#-----------------------------------------------------------------------------------------------------------------------------------


#View Booking Page  AKA VIEW_ALL_PUBLICATIONS.html
@app.route('/view_Booking_Page')
def view_Booking_Page():
    bookings = root.child('bookings').get()
    list = [] #store booking objects
    for typeid in bookings:

        eachbooking = bookings[typeid]

        if eachbooking['type'] == 'idoctor':
            doctor = Doctor(eachbooking['name'],eachbooking['age'],
                            eachbooking['phoneNumber'],eachbooking['email'],
                            eachbooking['startingDateAndTime'],eachbooking['type'],
                            eachbooking['specialization1'])
            doctor.set_typeid(typeid)
            print(doctor.get_typeid())
            list.append(doctor)
        else:
            instructor = Instructor(eachbooking['name'],eachbooking['age'],
                            eachbooking['phoneNumber'],eachbooking['email'],
                            eachbooking['startingDateAndTime'],eachbooking['type'],
                            eachbooking['specialization2'])
            instructor.set_typeid(typeid)
            print(instructor.get_typeid())
            list.append(instructor)

    return render_template('view_Booking_Page.html',bookings = list)


#Indicate what's needed for that form; for my radio field
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
#end

class bookingPage(Form):#aka class PublicationForm(Form)
    type = RadioField('Choose type  ',[validators.DataRequired()],choices=[('idoctor','Doctor'),('iinstructor','Instructor')],default="idoctor")
    name = StringField("Name (Mr/Ms/Madam) ",[validators.Length(min=1,max=150),validators.DataRequired()],default="Bojack Horseman")
    age = IntegerField("Age ",[validators.DataRequired()],default=54)
    phoneNumber = TextField("Number ",[validators.DataRequired()],default="08082716773") #kiv,will validate to sg number format
    email = EmailField("Email ", [validators.DataRequired(), validators.Email()],default="BoforGoJack@gmail.com")
    specialization1 = SelectField("Specialization(Doctors) ",[RequiredIf(type="idoctor")],choices=[("","Please Select:"),
                                                                                       ("Dermatology","Dermatology"),
                                                                                       ("General Medicine", "General Medicine"),
                                                                                       ("Internal Medicine", "Internal Medicine"),
                                                                                       ("Neurologist", "Neurologist"),],
                                                                                        default="")
    specialization2 =SelectField("Specialization(Instructors) ",[RequiredIf(type="iinstructor")],choices=[("","Please Select:"),
                                                                                           ("Yoga", "Yoga Instructor"),
                                                                                           ("Zumba", "Zumba Instructor"),
                                                                                           ("Hiphop", "Hip Hop Instructor"),
                                                                                           ("Piloxing", "Masala Bhangra Instructor")],
                                                                                            default="")
    # startingDateAndTime = DateTimeField("Starting Date & Time ",[validators.DataRequired()], format='%Y-%m-%d %H:%M:%S')
    startingDateAndTime = TextField("Starting Date & Time ", [validators.DataRequired()])
#credit card page
    cardType = RadioField('Payment Details  ',[validators.DataRequired()],choices=[('ivisa','Visa'),('imastercard','Master Card'),('iamericanexpress','American Express')],default="ivisa")
    cardName = StringField("Card Name ",[validators.Length(min=1,max=150),validators.DataRequired()])
    cardNumber = IntegerField("Card Number ",[validators.DataRequired()])
    expirationMonth = SelectField("Expiration Date ",[validators.DataRequired()],choices=[("","Please Select:"),
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
    expirationYear = SelectField("Expiration Year ",[validators.DataRequired()],choices=[("","Please Select:"),
                                                                                       ("2017","2017"),
                                                                                       ("2018", "2018"),
                                                                                       ("2019", "2019"),
                                                                                       ("2020", "2020"),
                                                                                       ("2021","2021"),
                                                                                       ("2022","2022"),
                                                                                       ("2023","2023")],
                                                                                        default="")
    cvcode = IntegerField("Card CV ",[validators.DataRequired()])
#Book Booking Page aka create_publications
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

            doctor = Doctor(name,age,phoneNumber,email,startingDateAndTime,type,specialization1)

            book_db = root.child('bookings')

            book_db.push({
                'name': doctor.get_name(),
                'age': doctor.get_age(),
                'phoneNumber': doctor.get_phoneNumber(),
                'email': doctor.get_email(),
                'startingDateAndTime': doctor.get_startingDateAndTime(),
                'type': doctor.get_type(),
                'specialization1': doctor.get_specialization1(),
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

            instructor = Instructor(name,age,phoneNumber,email,startingDateAndTime,type,specialization2)

            book_db = root.child('bookings')
            book_db.push({
                'name' : instructor.get_name(),
                'age' : instructor.get_age(),
                'phoneNumber' : instructor.get_phoneNumber(),
                'email' : instructor.get_email(),
                'startingDateAndTime' : instructor.get_startingDateAndTime(),
                'type' : instructor.get_type(),
                'specialization2' : instructor.get_specialization2()
            })

            flash('Your appointment is registered.', 'success')

        return redirect(url_for('view_Booking_Page'))
        # return render_template('view_Booking_Page.html',form=form)
    return render_template('Booking_Page.html', form=form)


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

            doctor = Doctor(name,age,phoneNumber,email,startingDateAndTime,type,specialization1)

            book_db = root.child('bookings/'+id)

            book_db.set({
                'name': doctor.get_name(),
                'age': doctor.get_age(),
                'phoneNumber': doctor.get_phoneNumber(),
                'email': doctor.get_email(),
                'startingDateAndTime': doctor.get_startingDateAndTime(),
                'type': doctor.get_type(),
                'specialization1': doctor.get_specialization1(),
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

            instructor = Instructor(name,age,phoneNumber,email,startingDateAndTime,type,specialization2)

            book_db = root.child('bookings/'+id)

            book_db.set({
                'name' : instructor.get_name(),
                'age' : instructor.get_age(),
                'phoneNumber' : instructor.get_phoneNumber(),
                'email' : instructor.get_email(),
                'startingDateAndTime' : instructor.get_startingDateAndTime(),
                'type' : instructor.get_type(),
                'specialization2' : instructor.get_specialization2(),
            })

            flash('Your appointment is registered.', 'success')

        return redirect(url_for('view_Booking_Page'))
    else:
        url = 'bookings/' + id
        eachbook = root.child(url).get()

        if eachbook['type'] == 'idoctor':
            doctor = Doctor(eachbook['name'],eachbook['age'],
                            eachbook['phoneNumber'],eachbook['email'],
                            eachbook['startingDateAndTime'],eachbook['type'],
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
                                    eachbook['startingDateAndTime'], eachbook['type'],
                                    eachbook['specialization2'])
            instructor.set_typeid(id)
            form.name.data = instructor.get_name()
            form.age.data = instructor.get_age()
            form.phoneNumber.data = instructor.get_phoneNumber()
            form.email.data = instructor.get_email()
            form.specialization2.data = instructor.get_specialization2()
            form.startingDateAndTime.data = instructor.get_startingDateAndTime()
            form.type.data = instructor.get_type()
        return render_template('update_Booking_Page.html',form=form)
    # return redirect(url_for("view_Booking_Page"))
#cancel appointment
@app.route('/delete_bookings/<string:id>',methods = ['POST'])
def delete_booking(id):
    book_db = root.child('bookings/'+id)
    book_db.delete()
    flash('Appoinment Cancelled','success')

    return redirect(url_for('view_Booking_Page'))




if __name__ == '__main__':
    app.secret_key = "helloworld"
    app.run()
