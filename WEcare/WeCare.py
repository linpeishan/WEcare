from flask import Flask, render_template, request, flash, redirect, url_for,session
from wtforms import Form, StringField, SelectField, IntegerField, RadioField, validators, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateTimeField
#--------------------------------------------------------------
from Login import Login
from ListOfNamesD import ListOfNamesD
from datetime import datetime
from Jo_Classes import QueryPage
from Jo_Classes import FitnessArticle
from Jo_Classes import DietaryArticle
from Jo_Classes import EnquiryAnswers

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
@app.route('/home')
def home():
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

if __name__ == '__main__':
    app.secret_key = "helloworld"
    app.run()