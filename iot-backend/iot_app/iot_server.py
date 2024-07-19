from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from DataBase import DatabaseService

from iot_base.rest_api import iot_blueprint

db = SQLAlchemy()


def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DatabaseService().db_url
    # Initialize extensions
    db.init_app(application)
    application.register_blueprint(iot_blueprint, url_prefix='/iot_events')

    return application


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
