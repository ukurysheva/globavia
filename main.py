from flask import Flask, render_template, request, redirect
import json

from conf.config import Config

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

URL = Config.URL
HEADERS = Config.HEADERS


##USER PAGES

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')


@app.route('/user/purchases', methods=('GET', 'POST'))
def purchases():
    return render_template('buy_ticket.html')


@app.route('/user/login', methods=('GET', 'POST'))
def login():
    body_register = {
        "userEmail": "",
        "userPassword": "",
        "userFirstName": "",
        "userLastName": "",
        "userPhoneNum": "",
        "birthDate": ""
    }
    body_login = {
        "email": "",
        "password": ""
    }

    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.form.get('firstname') is None:
            body_login['email'] = request.form['email']
            body_login['password'] = request.form['password']
            print("Logged")
            # requests.post(URL, headers=HEADERS, data=data)
            return redirect('/personal_cabinet')
        else:
            body_register['userEmail'] = request.form['email']
            body_register['userPassword'] = request.form['password']
            body_register['userFirstName'] = request.form['firstname']
            body_register['userLastName'] = request.form['lastname']
            body_register['userPhoneNum'] = request.form['phone']
            body_register['birthDate'] = request.form['birthdate']
            print("Registered")
            # requests.post(URL, headers=HEADERS, data=data)
            return redirect('/personal_cabinet')


@app.route('/personal_cabinet', methods=('GET', 'POST'))
def personal_cabinet():
    return render_template('profile_edit_data_and_skills-Bootdey.com.html')


##ADMIN PAGES
@app.route('/admin/sign-in', methods=('GET', 'POST'))
def admin_login():
    if request.method == "GET":
        return render_template('index_admin.html')
    else:
        body = {"email": '', "password": ''}

        email = request.form.get("username")
        password = request.form.get("password")
        print("I'm here")
        print(email)
        print(password)
        if email == "admin@yandex.ru" and password == "123test":
            print("Now I'm here")
            body['email'] = email
            body['password'] = password
            # Формируем json
            data = json.dumps(body)
            print(data)

            # requests.post(URL, headers=HEADERS, data=data)
            return redirect('/admin/menu')
        else:
            print("Unfortunately I'm here")
            return redirect('/admin/sign-in')


@app.route('/admin/menu', methods=('GET', 'POST'))
def menu():
    if request.method == "GET":
        return render_template('menu.html')
    else:
        pass


@app.route('/admin/list', methods=('GET', 'POST'))
def list():
    return render_template('list.html')


@app.route('/admin/Adding', methods=('GET', 'POST'))
def adding():
    return render_template('Adding.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="localhost")
