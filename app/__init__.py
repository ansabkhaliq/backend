import os, json
from flask import Flask, jsonify
from flask_session import Session

# For more information on Flask application factories:
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/

# For more information on Flask sessions:
# https://flask-session.readthedocs.io/en/latest/
from werkzeug.exceptions import HTTPException


sess = Session()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sess.init_app(app)

    # Blueprint for auth routes in our app

    from app.Controller import UserController as auth_blueprint
    app.register_blueprint(auth_blueprint.user)

    # Blueprints for non-auth parts of app
    from .Controller import ProductController as product_blueprint
    app.register_blueprint(product_blueprint.product)

    from .Controller import OrderController as order_blueprint
    app.register_blueprint(order_blueprint.order)

    from .Controller import CustomerController as customer_blueprint
    app.register_blueprint(customer_blueprint.cust)

    # Register Exception handler
    app.register_error_handler(HTTPException, lambda e: (jsonify({'message': e.description}), e.code))

    return app
