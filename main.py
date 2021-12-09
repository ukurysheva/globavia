from typing import Optional

from flask import Flask, render_template, request, redirect, Response
import requests
import json
import logging

from conf.config import Config

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

URL = Config.URL
HEADERS = Config.HEADERS
http = 'http://gvapi:8000'

# ЛОГИРОВАНИЕ
# СМОТРЕТЬ ЛОГИ В ОНЛАЙН РЕЖИМЕ $ docker logs --follow 73676c6275f0
logger = logging.getLogger('globalavia')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
##USER PAGESx1

# id and tokens for user to understand about cabinet
id = None
access_token = None
refresh_token = None
profile = None
email_g = None
password_g = None


@app.route('/', methods=('GET', 'POST'))
def index():
    global id, access_token, refresh_token
    direction = "/user/login"
    if access_token is not None or id is not None:
        direction = "/personal_cabinet"
    if request.method == "GET":
        r = requests.get('http://gvapi:8000/v1/countries')
        data_hash = r.json()
        countries = data_hash["data"]
        # print(countries, flush=True)
        # print([li["countryName"] for li in countries], flush=True)

        return render_template('index.html', countries=countries, direction=direction)


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')


@app.route('/user/purchases', methods=('GET', 'POST'))
def purchases():
    return render_template('buy_ticket.html')


@app.route('/user/login', methods=('GET', 'POST'))
def login():
    global access_token, id, refresh_token, profile, email_g, password_g
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

    if request.method == "GET" and (access_token is None or id is None):
        return render_template('login.html')

    elif request.method == "GET" and (access_token is not None or id is not None):
        return redirect('/personal_cabinet')

    elif request.method == "POST":
        if request.form.get('firstname') is None:
            body_login['email'] = request.form['email']
            body_login['password'] = request.form['password']
            try:
                r = requests.post('http://gvapi:8000/v1/auth/user/sign-in', json=body_login)
                if r.ok:
                    data = json.loads(r.text)
                    access_token = data["access_token"]
                    refresh_token = data["refresh_token"]
                    headers = {
                        'Authorization': 'Bearer ' + access_token
                    }

                    response = requests.request("GET", 'http://gvapi:8000/v1/users', headers=headers)
                    profile = json.loads(response.text)

                return redirect('/personal_cabinet')
            except Exception:
                return redirect('/user/login')
        else:
            try:
                body_register['userEmail'] = request.form['email']
                body_register['userPassword'] = request.form['password']
                body_register['userFirstName'] = request.form['firstname']
                body_register['userLastName'] = request.form['lastname']
                body_register['userPhoneNum'] = request.form['phone']
                body_register['birthDate'] = request.form['birthdate']

                email_g = request.form['email']
                password_g = request.form['password']
                logger.info("Email and Password")
                logger.info(email_g + " " + password_g)

                r = requests.post('http://gvapi:8000/v1/auth/user/sign-up', json=body_register)
                if r.ok:
                    data = json.loads(r.text)
                    logger.debug(data)
                    id = data["id"]
                    return redirect('/personal_cabinet')

                print("Registered")
            except (ValueError, KeyError, TypeError) as error:
                print(error)
                resp = Response({"JSON Format Error."}, status=400, mimetype='application/json')
                return resp, redirect('/user/login')


@app.route('/personal_cabinet', methods=('GET', 'POST'))
def personal_cabinet():

    global profile, access_token, refresh_token, email_g, password_g
    body_login_register = {"email": email_g, "password": password_g}

    r = requests.post('http://gvapi:8000/v1/auth/user/sign-in', json=body_login_register)
    data_tokens = json.load(r.text)
    access_token = data_tokens["access_token"]
    refresh_token = data_tokens["refresh_token"]
    logger.info("Access token")
    logger.info(access_token)

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", 'http://gvapi:8000/v1/users', headers=headers)
    profile = json.loads(response.text)
    body_person = {
        "passportSeries": "",
        "passportNumber": "",
        "phoneNumber": "",
        "familyName": "",
        "firstName": "",
        "middleName": "",
        "email": "",
        "addressRegister": "",
        "addressAccommodation": ""
    }

    familyname: Optional[str] = request.form.get("familyname")
    firstname = request.form.get("firstname")
    middlename = request.form.get("middlename")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    seria_passport = request.form.get("seria_passport")
    number_passport = request.form.get("number_passport")
    address_register = request.form.get("address_register")
    address_accommodation = request.form.get("address_accommodation")

    # if request.method == "GET" and

    if request.method == "GET" and firstname is not None:
        name = familyname + " " + firstname[0] + ". " + middlename[0] + "."
        number_of_tickets = "0"

        return render_template('profile_edit_data_and_skills-Bootdey.com.html',
                               name=name, email=email, number_of_tickets=number_of_tickets)
    elif request.method == "GET":
        return render_template('profile_edit_data_and_skills-Bootdey.com.html')

    elif request.method == "POST":
        if request.form['submit_button'] == "Сохранить":
            body_person['familyName'] = familyname
            body_person['passportSeries'] = seria_passport
            body_person['passportNumber'] = number_passport
            body_person['phoneNumber'] = phone_number
            body_person['firstName'] = firstname
            body_person['middleName'] = middlename
            body_person['email'] = email
            body_person['addressRegister'] = address_register
            body_person['addressAccommodation'] = address_accommodation

            data = json.dumps(body_person)

            # requests.post(URL, headers=HEADERS, data=data)
            return redirect('/personal_cabinet')


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
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
