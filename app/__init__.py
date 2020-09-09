import os
from flask import Flask
from flask_session import Session

# For more information on Flask application factories:
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/

# For more information on Flask sessions:
# https://flask-session.readthedocs.io/en/latest/


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
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
