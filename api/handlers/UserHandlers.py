import logging

from flask import request, jsonify, render_template, app
from flask_restful import Resource

import api.errors.errors as error
from api.conf.auth import access_token, refresh_token, refresh_jwt


class Index(Resource):
    @app.route(defaults={'file': 'index.html'})
    @staticmethod
    def index():
        return render_template('index.html')


class Register(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            username, password, email = (
                request.json.get("username").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Return success if registration is completed.
        return {"status": "registration completed."}


class CreateUser:
    @staticmethod
    def post():

        try:
            # Get admin email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )
            print(email)
            print(password)

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if admin information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Generate refresh token.
        refresh_tokens = refresh_jwt.dumps({"email": email})
        print(refresh_tokens)

        # Return access token and refresh token.
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


class LoginUser:
    def post(self):
        pass


class LogoutUser:
    def post(self):
        pass


class RefreshToken:
    def post(self):
        pass


class InfoAcc:
    def get(self):
        return


class ChangeInfoAcc:
    def post(self):
        pass


class CreatePurchase:
    def post(self):
        pass


class GetPurchase:
    def get(self):
        pass
