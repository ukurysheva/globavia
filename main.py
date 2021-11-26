from flask import Flask, render_template

from api.conf.routes import generate_routes


def create_app():
    # Create a flask api.
    app = Flask(__name__, template_folder='template')

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    # Set database url.
    # app.config['PREFERRED_URL_SCHEME'] = Config.URL

    # Generate routes.
    #generate_routes(app)

    @app.route("/")
    def home():
        return render_template('index.html')

    @app.route("/about/")
    def about():
        return render_template('contact.html')

    # Return api.
    return app


if __name__ == '__main__':
    # Create api.
    app = create_app()

    # Run api. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, #host='localhost',
            use_reloader=True)
