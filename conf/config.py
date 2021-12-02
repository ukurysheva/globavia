import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SETUP_CFG = os.path.join(os.path.dirname(__file__), '../../setup.cfg')
    HOST = "/etc/hosts"
    IP_ADRESS = "62.152.63.25"
    REFFERENCE = "www.globalavia-api.ru"
    URL = "globalavia-api.ru:8000/"
    HEADERS = ''
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'templates/static'), ]

