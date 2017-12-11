from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextField, SelectField, IntegerField, DateTimeField, validators, RadioField
from wtforms.fields.html5 import EmailField
import doctor as doctor
import instructor as instructor
#firebase stuffs
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/booking-b814e-firebase-adminsdk-j8prf-51aedf5eb9.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://booking-b814e.firebaseio.com/'
})

root = db.reference()




app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/videoChat')
def videoChat():
    return render_template('VideoChat.html')

#View Booking Page  AKA VIEW_ALL_PUBLICATIONS
@app.route('/viewBookings')
def viewBookings():
    return render_template('view_Booking_Page.html')

#start
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
    name = StringField("Name (Mr/Ms/Madam) ",[validators.Length(min=1,max=150),validators.DataRequired()])
    age = IntegerField("Age ",[validators.DataRequired(),validators.Length(200)])
    phoneNumber = TextField("Number ",[validators.DataRequired()]) #kiv,will validate to sg number format
    email = EmailField("Email ", [validators.DataRequired(), validators.Email()])
    specialization1 = SelectField("Specialization(Doctors) ",[RequiredIf(type="idoctor")],choices=[("","Please Select:"),
                                                                                       ("ddermatology","Dermatology"),
                                                                                       ("dgeneralmedicine", "General Medicine"),
                                                                                       ("dinternalmedicine", "Internal Medicine"),
                                                                                       ("dneurologist", "Neurologist"),],
                                                                                        default="")
    specialization2 =SelectField("Specialization(Instructors) ",[RequiredIf(type="iinstructor")],choices=[("","Please Select:"),
                                                                                           ("iyoga", "Yoga Instructor"),
                                                                                           ("izumba", "Zumba Instructor"),
                                                                                           ("ihiphop", "Hip Hop Instructor"),
                                                                                           ("ipiloxing", "Masala Bhangra Instructor")],
                                                                                            default="")
    startingDateAndTime = DateTimeField("Starting Date & Time ",[validators.DataRequired()], format='%Y-%m-%d %H:%M:%S')

#Book Booking Page aka create_publications
@app.route('/bookingPage',methods=["GET","POST"]) #@app.route('/newpublication')
def bookingpage():
    form = bookingPage(request.form)
    if request.method == "POST" and form.validate():
        if form.type.data == "idoctor":
            name = form.name.data
            age = form.age.data
            phoneNumber = form.phoneNumber.data
            email = form.email.data
            specialization = form.specialization1.data
            dateAndTime = form.dateAndTime.data

            doc = doctor.Doctor(name,age,phoneNumber,email,dateAndTime,specialization)

            doc_db = root.child('Doctor')
            doc_db.push({
                'Name': doc.get_name(),
                'Age' : doc.get_age(),
                'Phone Number' : doc.get_phoneNumber(),
                'Email' : doc.get_email(),
                'Date And Time' : doc.get_dateAndTime(),
                'Specialization' : doc.get_specialization()
            })

            flash('Doctor Appointment Booked.','success')

        elif form.type.data == "iinstructor":
            name = form.name.data
            age = form.age.data
            phoneNumber = form.phoneNumber.data
            email = form.email.data
            specialization = form.specialization2.data
            dateAndTime = form.dateAndTime.data

            ins = instructor.Instructor(name,age,phoneNumber,email,dateAndTime,specialization)

            ins_db = root.child('Instructor')
            ins_db.push({
                'Name' : ins.get_name(),
                'Age' : ins.get_age(),
                'Phone Number' : ins.get_phoneNumber(),
                'Email' : ins.get_email(),
                'Date And Time' : ins.get_dateAndTime(),
                'Specialization' : ins.get_specialization()
            })

            flash('Instructor Appointment Booked.','success')

        return redirect(url_for('view_Booking_Page.html'))
        # return render_template('Booking_Page.html',form=form)
    return render_template('Booking_Page.html', form=form)


#update/ change date and time aka update_publications
@app.route('/update')
def update_bookings():
    form = bookingPage(request.form)
    form.username.data = "BojackHorseMan"
    form.name.data = "BoJack HorseMan"
    form.age.data = 54
    form.phoneNumber.data = "6116162"
    form.email.data = "bojack@gmail.com"
    form.specialization.data = "Dermatology"
    return render_template('update_Booking_Page.html',form=form)


if __name__ == '__main__':
    app.secret_key = "helloworld"
    app.run()
