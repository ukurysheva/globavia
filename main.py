from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

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

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


@app.route('/', methods=('GET', 'POST'))
def index():

    return render_template('index.html')


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')

