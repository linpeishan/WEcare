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

@app.route('/')
def home():
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
            flash(doctor.get_name()+" has booked "+doctor.get_specialization1()+" on "+doctor.get_startingDateAndTime()+". Click 'Appointment Details' to find out more.",'success')
        elif eachbooking['type'] == 'iinstructor':
            instructor = Instructor(eachbooking['name'],eachbooking['age'],
                            eachbooking['phoneNumber'],eachbooking['email'],
                            eachbooking['startingDateAndTime'],eachbooking['type'],
                            eachbooking['specialization2'])
            instructor.set_typeid(typeid)
            print(instructor.get_typeid())
            list.append(instructor)
            flash(instructor.get_name()+" has booked "+instructor.get_specialization2()+" on "+instructor.get_startingDateAndTime()+". Click 'Appointment Details' to find out more.",'success')


    return render_template('home.html',bookings = list)
@app.route('/videoChat')
def videoChat():
    return render_template('VideoChat.html')
@app.route('/tips-dietary')
def tipsdietary():
    return render_template('healthtips_dietary.html')
@app.route('/tips-fitness')
def tipsfitness():
    return render_template('healthtips_fitness.html')
@app.route('/doctors-allergist')
def doctorsAllergist():
    return render_template('allergist.html')
@app.route('/doctors-anesthesiologist')
def doctorsAnesthesiologist():
    return render_template('anesthesiologist.html')
@app.route('/doctors-audiologist')
def doctorsAudiologist():
    return render_template('audiologist.html')
@app.route('/doctors-cardiologist')
def doctorsCardiologist():
    return render_template('cardiologist.html')
@app.route('/doctors-dentist')
def doctorsDentist():
    return render_template('dentist.html')
@app.route('/trainers-yoga')
def trainersYoga():
    return render_template('trainers_yoga.html')
@app.route('/trainers-zumba')
def trainersZumba():
    return render_template('trainers_zumba.html')
@app.route('/reviews')
def reviews():
    return render_template('reviews.html')
@app.route('/dietary-tip1')
def dietarytip1():
    return render_template('dietarytip1.html')
@app.route('/dietary-tip2')
def dietarytip2():
    return render_template('dietarytip2.html')
@app.route('/dietary-tip3')
def dietarytip3():
    return render_template('dietarytip3.html')
@app.route('/fitness-tip1')
def fitnesstip1():
    return render_template('fitnesstip1.html')
@app.route('/fitness-tip2')
def fitnesstip2():
    return render_template('fitnesstip2.html')
@app.route('/fitness-tip3')
def fitnesstip3():
    return render_template('fitnesstip3.html')
@app.route('/chatpage')
def chatPage():
    return render_template('chat_box - Compiled.html')
@app.route('/end')
def end():
    return render_template('End.html')
@app.route('/login')
def login():
    return render_template('Login.html')
@app.route('/register')
def register():
    return render_template('RegisterPage.html')
@app.route('/profile')
def profile():
    return render_template('Profile.html')
@app.route('/t&c')
def t_and_c():
    return render_template('T&Cs.html')
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
        elif eachbooking['type'] == 'iinstructor':
            instructor = Instructor(eachbooking['name'],eachbooking['age'],
                            eachbooking['phoneNumber'],eachbooking['email'],
                            eachbooking['startingDateAndTime'],eachbooking['type'],
                            eachbooking['specialization2'])
            instructor.set_typeid(typeid)
            print(instructor.get_typeid())
            list.append(instructor)
        else:
            flash("You have no appointments.")
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
class QueryPage():
    def _init__(self, query):
        self._query = query

    def get_query(self):
        return self._query

    def set_query(self, query):
        self._query= query

class queryPage(Form):
    query = TextField("Query", [validators.DataRequired()])
    specialization = SelectField("Specialization",[validators.DataRequired()],choices=[("","Please Select"),
                                                               ("danesthesiologist","Anesthesiologist"),
                                                               ("dallergist", "Allergist"),
                                                               ("daudiologist", "Audiologist"),
                                                               ("dcardiologist", "Cardiologist"),
                                                               ("dcardiologist", "Cardiologist"),],
                                                                default="")
@app.route('/query', methods=['GET', 'POST'])
def query():
    form = queryPage(request.form)
    if request.method == 'POST' and form.validate():
        query = form.query.data
        newquery = QueryPage(query)
        newquery_sent = root.child('queries')
        newquery_sent.push({
            'query': newquery.get_query()
        })
        flash('Magazine Inserted Sucessfully.', 'success')

        return render_template('home.html', form=form)
    return render_template('QueryPage.html', form=form)

class bookingPage(Form):#aka class PublicationForm(Form)
    type = RadioField('Choose type  ',[validators.DataRequired()],choices=[('idoctor','Doctor'),('iinstructor','Instructor')],default="idoctor")
    name = StringField("Name (Mr/Ms/Madam) ",[validators.Length(min=1,max=150),validators.DataRequired()],default="Bojack Horseman")
    age = IntegerField("Age ",[validators.DataRequired()],default=54)
    phoneNumber = TextField("Number ",[validators.DataRequired()],default="81345678") #kiv,will validate to sg number format
    email = EmailField("Email ", [validators.DataRequired(), validators.Email()],default="BoforGoJack@gmail.com")
    specialization1 = SelectField("Specialization(Doctors) ",[RequiredIf(type="idoctor")],choices=[("","Please Select:"),
                                                                                                   ("Andrew(Anesthesiologist)","Andrew(Anesthesiologist)"),
                                                                                                   ("Jack(Anesthesiologist)","Jack(Anesthesiologist)"),
                                                                                                   ("Jacob(Anesthesiologist)", "Jacob(Anesthesiologist)"),
                                                                                                   ("Jill(Anesthesiologist)", "Jill(Anesthesiologist)"),
                                                                                                   ("Johnny(Anesthesiologist)","Johnny(Anesthesiologist)"),
                                                                                                   ("Mason(Anesthesiologist)","Mason(Anesthesiologist)"),
                                                                                                   ("Noah(Anesthesiologist)","Noah(Anesthesiologist)"),
                                                                                                   ("Olivia(Anesthesiologist)","Olivia(Anesthesiologist)"),
                                                                                                   ("Zoe(Anesthesiologist)","Zoe(Anesthesiologist)"),
                                                                                                   ("Audrey(Allergist)","Audrey(Anesthesiologist)"),
                                                                                                   ("David(Allergist)","David(Allergist)"),
                                                                                                   ("Emma(Allergist)","Emma(Allergist)"),
                                                                                                   ("Marcus(Allergist)","Marcus(Allergist)"),
                                                                                                   ("Penelope(Allergist)","Penelope(Allergist)"),
                                                                                                   ("Sophia(Allergist)","Sophia(Allergist)"),
                                                                                                   ("Michael(Allergist)","Michael(Allergist)"),
                                                                                                   ("Chuan Lim(Audiologist)","Chuan Lim(Audiologist)"),
                                                                                                   ("Chloe(Audiologist)","Chloe(Audiologist)"),
                                                                                                   ("Emily(Audiologist)","Emily(Audiologist)"),
                                                                                                   ("Grace(Audiologist)","Grace(Audiologist)"),
                                                                                                   ("Isabella(Audiologist)","Isabella(Audiologist)"),
                                                                                                   ("Jayden(Audiologist)","Jayden(Audiologist)"),
                                                                                                   ("Luke(Audiologist)","Luke(Audiologist)"),
                                                                                                   ("Will Smith(Audiologist)","Will Smith(Audiologist)"),
                                                                                                   ("Adam(Dentist)","Adam(Dentist)"),
                                                                                                   ("Andrian(Dentist)","Andrian(Dentist)"),
                                                                                                   ("Aria(Dentist)","Aria(Dentist)"),
                                                                                                   ("Eva(Dentist)","Eva(Dentist)"),
                                                                                                   ("Hannah(Dentist)","Hannah(Dentist)"),
                                                                                                   ("Jamie Foxx(Dentist)","Jamie Foxx(Dentist)"),
                                                                                                   ("Jordan(Dentist)","Jordan(Dentist)"),
                                                                                                   ("Nicholas(Dentist)","Nicholas(Dentist)"),
                                                                                                   ("Spencer(Dentist)","Spencer(Dentist)"),
                                                                                                   ],
                                                                                                    default="")
    specialization2 =SelectField("Specialization(Instructors) ",[RequiredIf(type="iinstructor")],choices=[("","Please Select:"),
                                                                                                          ("Andian(Yoga)", "Andian(Yoga)"),
                                                                                                          ("Arthur(Yoga)","Arthur(Yoga)"),
                                                                                                          ("Aria(Yoga)","Aria(Yoga)"),
                                                                                                          ("Ashton(Yoga)","Ashton(Yoga)"),
                                                                                                          ("Ali(Yoga)","Ali(Yoga)"),("Cameron(Yoga)","Cameron(Yoga)"),
                                                                                                          ("Cameron(Yoga)","Cameron(Yoga)"),
                                                                                                          ("Hannah(Yoga)","Hannah(Yoga)"),
                                                                                                          ("Mary(Yoga)","Mary(Yoga)"),
                                                                                                          ("Samuel(Zumba)","Samuel(Yoga)"),
                                                                                                          ("Caleb(Zumba)","Caleb(Zumba)"),
                                                                                                          ("David(Zumba)","David(Zumba)"),
                                                                                                          ("Daniel(Zumba)","Daniel(Zumba)"),
                                                                                                          ("Dylan(Zumba)","Dylan(Zumba)"),
                                                                                                          ("Eden(Zumba)","Eden(Zumba)"),
                                                                                                          ("Edward(Zumba)","Edward(Zumba)"),
                                                                                                          ("Jim(Zumba)","Jim(Zumba)"),
                                                                                                          ("Rayson(Zumba)","Rayson(Zumba)"),

                                                                                                          ],
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

            flash("Your appointment has been rescheduled", 'success')

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

            flash('Your appointment has been rescheduled.', 'success')

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
