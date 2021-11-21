import os


class Config:
    SETUP_CFG = os.path.join(os.path.dirname(__file__), 'setup.cfg')
    OAUTH_CREDENTIALS = {
        "access_token": "eyJhbGciOiJIUzI1NiIsI",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJle"}
    SECRET_KEY = 'a really really really really long secret key'
    DATABASE_URI = 'smth'
    MAIL_SERVER = 'shop2u'
    MAIL_PORT = 111  # надо выбрать правильный
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'youmail@gmail.com'
    MAIL_DEFAULT_SENDER = 'youmail@gmail.com'
    MAIL_PASSWORD = 'password'
