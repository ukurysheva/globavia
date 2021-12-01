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

# Create User.
create_user = "/v1/auth/user/sign-up"

# Login page User.
login = "/v1/auth/user/sign-in"

# Logout page User.
logout = "/v1/auth/user/sign-out"

# Refresh token.
refresh = "/v1/auth/user/token/refresh"

# Get Information Page.
get_info = "/v1/users"

# Change Information Page.
change = "/v1/users"

# Create Purchase.
create_purchase = "/v1/users/purchases"

# Get Purchase by id.
get_purchase = "/v1/users/purchases/<int: id>"


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')


@app.route('/personal_cabinet', methods=('GET', 'POST'))
def personal_cabinet():
    return render_template('profile_edit_data_and_skills-Bootdey.com.html')


class AdminLogin(FlaskForm):
    username = StringField(label='Имя пользователя',
                           validators=[DataRequired()])

    password = StringField(label='Пароль',
                           validators=[DataRequired()])

    submit = SubmitField(label='войти')


##ADMIN PAGES
@app.route('/admin/sign-in', methods=('GET', 'POST'))
def admin_login():

    if request.method == "GET":
        return render_template('index_admin.html')
    else:
        body = {"email": '', "password": ''}

        # form = AdminLogin()
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

    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="localhost")
