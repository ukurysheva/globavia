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


@app.route('/', methods=('GET', 'POST'))
def index():

    return render_template('index.html')


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')

@app.route('/personal_cabinet', methods=('GET', 'POST'))
def personal_cabinet():
    return render_template('profile_edit_data_and_skills-Bootdey.com.html')


@app.route('/admin', methods=('GET', 'POST'))
def admin_login():
    return render_template('index_admin.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="localhost")