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
# USER
id_user = None
access_token_user = None
refresh_token_user = None
profile_user = None
email_g_user = None
password_g_user = None
passport_series = " Серия паспорта"
passport_number = "Номер паспорта"
phone_number = "Номер телефона"
address_register = "Место регистрации"
address_accommodation = "Фактическое место проживания"
middlename = "Отчество"
number_of_tickets = 0

# ADMIN
id_admin = None
access_token_admin = None
refresh_token_admin = None
profile_admin = None
email_g_admin = None
password_g_admin = None


@app.route('/', methods=('GET', 'POST'))
def index():
    global id_user, access_token_user, refresh_token_user
    direction = "/user/login"
    if access_token_user is not None or id_user is not None:
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
    global access_token_user, id_user, refresh_token_user, profile_user, email_g_user, password_g_user
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

    if request.method == "GET" and (access_token_user is None or id_user is None):
        return render_template('login.html')

    elif request.method == "GET" and (access_token_user is not None or id_user is not None):
        return redirect('/personal_cabinet')

    elif request.method == "POST":
        if request.form.get('firstname') is None:
            body_login['email'] = request.form['email']
            body_login['password'] = request.form['password']
            try:
                r = requests.post('http://gvapi:8000/v1/auth/user/sign-in', json=body_login)
                if r.ok:
                    data = json.loads(r.text)
                    access_token_user = data["access_token"]
                    refresh_token_user = data["refresh_token"]
                    headers = {
                        'Authorization': 'Bearer ' + access_token_user
                    }

                    response = requests.request("GET", 'http://gvapi:8000/v1/users', headers=headers)
                    profile_user = json.loads(response.text)

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

                email_g_user = request.form['email']
                password_g_user = request.form['password']
                logger.info("Email and Password")
                logger.info(email_g_user + " " + password_g_user)

                body_login_register = {"email": email_g_user, "password": password_g_user}

                r = requests.post('http://gvapi:8000/v1/auth/user/sign-up', json=body_register)
                if r.ok:
                    data = json.loads(r.text)
                    logger.debug(data)
                    id_user = data["id"]

                    req = requests.post('http://gvapi:8000/v1/auth/user/sign-in', json=body_login_register)
                    data_tokens = json.loads(req.text)
                    access_token_user = data_tokens["access_token"]
                    refresh_token_user = data_tokens["refresh_token"]
                    logger.info("Access token")
                    logger.info(access_token_user)

                    headers = {
                        'Authorization': 'Bearer ' + access_token_user
                    }

                    response = requests.request("GET", 'http://gvapi:8000/v1/users', headers=headers)
                    profile_user = json.loads(response.text)

                    return redirect('/personal_cabinet')

                print("Registered")
            except (ValueError, KeyError, TypeError) as error:
                print(error)
                resp = Response({"JSON Format Error."}, status=400, mimetype='application/json')
                return resp, redirect('/user/login')


@app.route('/personal_cabinet', methods=('GET', 'POST'))
def personal_cabinet():
    global profile_user, access_token_user, refresh_token_user, email_g_user, \
        password_g_user, passport_number, passport_series, number_of_tickets, \
        address_register, address_accommodation, phone_number

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

    familyname: Optional[str] = profile_user["userLastName"]
    firstname = profile_user["userFirstName"]
    middlename = request.form.get("middlename")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    passport_series = request.form.get("seria_passport")
    passport_number = request.form.get("number_passport")
    address_register = request.form.get("address_register")
    address_accommodation = request.form.get("address_accommodation")

    if request.method == "GET":
        name = profile_user['userLastName'] + " " + profile_user["userFirstName"][0].upper() + "."
        email = profile_user['userEmail']

        return render_template('profile_edit_data_and_skills-Bootdey.com.html',
                               name=name, email=email, number_of_tickets=number_of_tickets,
                               familyname=familyname, firstname=firstname, middlename=middlename,
                               phone_number=phone_number, passport_series=passport_series,
                               passport_number=passport_number, address_register=address_register,
                               address_accommodation=address_accommodation)

    elif request.method == "POST":
        logger.info("after post")
        if request.form['submit_button'] == "Сохранить":
            logger.info("after_submit")
            body_person['familyName'] = familyname
            body_person['passportSeries'] = passport_series
            body_person['passportNumber'] = passport_number
            body_person['phoneNumber'] = phone_number
            body_person['firstName'] = firstname
            body_person['middleName'] = middlename
            body_person['email'] = email
            body_person['addressRegister'] = address_register
            body_person['addressAccommodation'] = address_accommodation

            headers = {
                'Authorization': 'Bearer ' + access_token_user
            }
            logger.info("Trying to send")
            response = requests.request("POSY", 'http://gvapi:8000/v1/users', headers=headers, params=body_person)
            if response.ok:
                logger.info("OK")
                logger.info(response.text)
                return redirect("/personal cabinet")


##ADMIN PAGES
@app.route('/admin/sign-in', methods=('GET', 'POST'))
def admin_login():
    global access_token_admin, id_admin, refresh_token_admin, profile_admin, email_g_admin, password_g_admin

    if request.method == "GET" and (access_token_admin is None or id_admin is None):
        return render_template('index_admin.html')
    elif request.method == "GET" and (access_token_admin is not None or id_admin is not None):
        return redirect('/admin/menu')
    elif request.method == "POST":

        body_login = {"email": request.form.get("username"), "password": request.form.get("password")}

        email_g_admin = request.form.get("username")
        password_g_admin = request.form.get("password")

        r = requests.post('http://gvapi:8000/v1/auth/admin/sign-in', json=body_login)
        logger.info("I'm here")
        logger.info(r.status_code)
        if r.ok:
            data_tokens = json.loads(r.text)
            access_token_admin = data_tokens['access_token']
            refresh_token_admin = data_tokens['refresh_token']
            logger.info("access_tokens")
            logger.info(access_token_admin)

            return redirect('/admin/menu')
        else:
            return redirect("/admin/sign-in")


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
