import os

from flask import Flask

from api.conf.config import Config
from api.conf.routes import generate_routes


def create_app():

    # Create a flask api.
    app = Flask(__name__)

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    # Set database url.
    #app.config['PREFERRED_URL_SCHEME'] = Config.URL


    # Generate routes.
    generate_routes(app)

    # Return api.
    return app


if __name__ == '__main__':

    # Create api.
    app = create_app()

    # Run api. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)