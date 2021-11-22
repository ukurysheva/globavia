import os

from flask import Flask

from api.conf.config import Config
from api.conf.routes import generate_routes
from api.database.database import db
from api.db_initializer.db_initializer import (create_admin_user,
                                               create_super_admin,
                                               create_test_user)


def create_app():

    # Create a flask api.
    app = Flask(__name__)

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    # Set database url.
    app.config['DATABASE_URI'] = Config.DATABASE_URI

    app.config['TRACK_MODIFICATIONS'] = True

    # Generate routes.
    generate_routes(app)

    # Database initialize with api.
    db.init_app(app)

    # Check if there is no database.
    if not os.path.exists(Config.DATABASE_URI):

        # New db api if no database.
        db.app = app

        # Create all database tables.
        db.create_all()

        # Create default super admin user in database.
        create_super_admin()

        # Create default admin user in database.
        create_admin_user()

        # Create default test user in database.
        create_test_user()

    # Return api.
    return app


if __name__ == '__main__':

    # Create api.
    app = create_app()

    # Run api. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)