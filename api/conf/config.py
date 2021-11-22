import os




#basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Create a database in project and get it's path.
#SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")

class Config:
    SETUP_CFG = os.path.join(os.path.dirname(__file__), '../../setup.cfg')
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
