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
    global access_token_user

    if (request.method == "GET" or request.method == "POST") and access_token_user is not None:
        return render_template('buy_ticket.html')
    else:
        return redirect('/user/login')


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

    if (request.method == "GET" or request.method == "POST") and access_token_user is not None:

        body_person = {
            "email": ""
        }

        familyname: Optional[str] = profile_user["userLastName"]
        firstname = profile_user["userFirstName"]

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

            phone_number = request.form.get("phone_number")
            passport_series = request.form.get("seria_passport")
            passport_number = request.form.get("number_passport")
            address_register = request.form.get("address_register")
            address_accommodation = request.form.get("address_accommodation")

            body_person["email"] = request.form.get("email")

            headers = {
                'Authorization': 'Bearer ' + access_token_user
            }
            logger.info("Trying to send")
            logger.info(headers)
            response = requests.request("POST", 'http://gvapi:8000/v1/users', headers=headers, json=body_person)

            if response.ok:
                logger.info("OK")
                logger.info(response.text)
                return redirect("/personal_cabinet")
            else:
                logger.info("Not OK")
                return redirect("/personal_cabinet")
    else:
        return redirect("/user/login")


##ADMIN PAGES
@app.route('/admin/sign-in', methods=('GET', 'POST'))
def admin_login():
    global access_token_admin, id_admin, refresh_token_admin, \
        profile_admin, email_g_admin, password_g_admin

    access_token_admin = None
    refresh_token_admin = None

    if request.method == "GET" and (access_token_admin is None or id_admin is None):
        return render_template('index_admin.html')
    elif request.method == "GET" and (access_token_admin is not None or id_admin is not None):
        return redirect('/admin/menu')
    elif request.method == "POST":

        body_login = {"email": request.form["username"], "password": request.form["password"]}

        email_g_admin = body_login["email"]
        password_g_admin = body_login["password"]

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
    global access_token_admin, id_admin, refresh_token_admin, \
        profile_admin, email_g_admin, password_g_admin

    data_countries = {}
    data_airports = {}
    data_aviacompanies = {}
    data_planes = {}
    data_flights = {}
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('menu.html')
        elif request.method == "GET":
            pass
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/adding/country', methods=('GET', 'POST'))
def adding_country():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:
        if request.method == "GET":
            return render_template('adding_country.html')
        else:
            country_id = request.form.get("country_id")
            name = request.form.get("name")
            continent = request.form.get("continent")
            country_wiki = request.form.get("country_wiki")

            return redirect("/admin/adding/country")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/adding/airport', methods=('GET', 'POST'))
def adding_airport():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:
        if request.method == "GET":
            return render_template('adding_airport.html')
        else:
            country_id = request.form.get("country_id")
            name = request.form.get("name")
            continent = request.form.get("continent")
            country_wiki = request.form.get("country_wiki")

            return redirect("/admin/adding/airport")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/adding/plane', methods=('GET', 'POST'))
def adding_plane():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('adding_plane.html')
        else:
            aircraftIata = request.form.get("aircraftIata")
            aircraftName = request.form.get("aircraftName")
            aircraftManufacturer = request.form.get("aircraftManufacturer")
            aircraftType = request.form.get("aircraftType")

            aircraftIcaic = request.form.get("aircraftIcaic")
            aircraftWingType = request.form.get("aircraftWingType")
            economyClass = request.form.get("economyClass")
            prEconomyClass = request.form.get("prEconomyClass")

            businessClass = request.form.get("businessClass")
            firstClass = request.form.get("firstClass")

            return redirect("/admin/adding/plane")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/adding/flight', methods=('GET', 'POST'))
def adding_flight():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('adding_flight.html')
        else:
            flightName = request.form.get("flightName")
            airlineId = request.form.get("airlineId")
            ticketNumEconomy = request.form.get("ticketNumEconomy")
            ticketNumPrEconomy = request.form.get("ticketNumPrEconomy")

            ticketNumBusiness = request.form.get("ticketNumBusiness")
            ticketNumFirstClass = request.form.get("ticketNumFirstClass")
            costRubEconomy = request.form.get("costRubEconomy")
            costRubPrEconomy = request.form.get("costRubPrEconomy")

            costRubBusiness = request.form.get("costRubBusiness")
            costRubFirstClass = request.form.get("costRubFirstClass")

            aircraftId = request.form.get("aircraftId")
            airportDepId = request.form.get("airportDepId")
            airportLandId = request.form.get("airportLandId")
            departureTime = request.form.get("departureTime")

            landingTime = request.form.get("landingTime")
            maxLuggageWeightKg = request.form.get("maxLuggageWeightKg")
            costLuggageWeightRub = request.form.get("costLuggageWeightRub")
            maxHandLuggageWeightKg = request.form.get("maxHandLuggageWeightKg")

            costHandLuggageWeightRub = request.form.get("costHandLuggageWeightRub")
            wifiFlg = request.form.get("wifiFlg")
            foodFlg = request.form.get("foodFlg")
            usbFlg = request.form.get("usbFlg")

            return redirect("/admin/adding/flight")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/adding/aviacompany', methods=('GET', 'POST'))
def adding_aviacompany():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('adding_aviacompany.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/adding/aviacompany")
    else:
        return redirect('/admin/sign-in')


# LIST

@app.route('/admin/list/airport', methods=('GET', 'POST'))
def get_airport():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('list_airport.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/list/airport")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/list/aviacompany', methods=('GET', 'POST'))
def get_aviacompany():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('list_aviacompany.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/list/aviacompany")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/list/country', methods=('GET', 'POST'))
def get_country():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('list_country.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/list/country")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/list/flight', methods=('GET', 'POST'))
def get_flight():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('list_flight.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/list/flight")
    else:
        return redirect('/admin/sign-in')


@app.route('/admin/list/plane', methods=('GET', 'POST'))
def get_plane():
    global access_token_admin
    if (request.method == "GET" or request.method == "POST") and access_token_admin is not None:

        if request.method == "GET":
            return render_template('list_plane.html')
        else:
            aviacompany_id = request.form.get("aviacompany_id")
            airlineIata = request.form.get("airlineIata")
            airlineIcao = request.form.get("airlineIcao")
            aviacompany_status = request.form.get("aviacompany_status")

            return redirect("/admin/list/plane")
    else:
        return redirect('/admin/sign-in')


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
