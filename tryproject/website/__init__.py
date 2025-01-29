from flask import Flask
from flask_pymongo import PyMongo
from pymisp import ExpandedPyMISP
from .config import Config

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    with app.app_context():
        app.misp = ExpandedPyMISP(
            app.config['MISP_URL'],
            app.config['MISP_KEY'],
            app.config['MISP_VERIFYCERT']
        )

    from .views import main
    app.register_blueprint(main)

    return app
