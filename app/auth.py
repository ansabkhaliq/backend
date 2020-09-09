import os
import logging
from flask import Blueprint, request, jsonify, session
from Resource.IAM import SQUIZZConnectionHelper
from Resource.UserResource import UserResource
import app.main as main

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Configure Flask application
base_url = os.environ.get('BASE_URL')
auth = Blueprint('auth', __name__)


# Initialise database resource objects
user_resource = UserResource()


# -- Helper functions
def validate_login_session():
    """
    Determine whether or not the current user 
    has an existing session within the database

    Args:
        None
    """
    login_session = session.get('login_session')
    org_id = session.get('org_id')

    if user_resource.validate_session(login_session, org_id):
        return True
    return False


def build_connection():
    """
    Builds an returns an object that represents 
    a connection to the SQUIZZ platform

    Args:
        None
    """
    # Retrieve organisation API key and password from the database
    org_id = session.get('org_id')
    api_org_key, api_org_pw = user_resource.retrieve_api_key_pw(org_id)

    return SQUIZZConnectionHelper(base_url, org_id, api_org_key, api_org_pw)


# -- Application routes
@auth.route('/login')
def login():
    if validate_login_session():
        return main.index()
    return "login page here", 200


@auth.route('/api/login', methods=['POST'])
def login_post():
    if validate_login_session():
        result = {'status': "success", 'data': {"session_id": session.get('login_session')}, "message": "LOGIN_EXIST"}
        return jsonify(result)

    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')

    try:
        org_id = user_resource.validate_username_password(username, password)
    except AttributeError:
        result = {'status': "failure", 'data': {"session_id": None}, "message": "LOGIN_WRONG"}
        return jsonify(result)

    if org_id is None:
        #wrong username or password
        result = {'status': "failure", 'data': {"session_id": None}, "message": "LOGIN_WRONG"}
        return jsonify(result)
    
    session['org_id'] = org_id
    connection = build_connection()
    session_id, status_code = connection.create_session()
    if status_code == "LOGIN_SUCCESS":
        session.permanent = True
        session['seesion_id'] = session_id
        session['login_session'] = session_id
        user_resource.store_session(session_id, org_id)
        logger.info(f"Created a new login session with ID: {session_id}")
        result = {'status': "success", 'data': {"session_id": session_id}, "message": "LOGIN_SUCCESS"}
        return jsonify(result)
    else:
        result = {'status': "failure", 'data': {"session_id": None}, "message": status_code}
        return jsonify(result) 

@auth.route('/api/logout', methods=['GET'])
def logout():
    login_session = session.get('login_session')
    if validate_login_session():
        user_resource.remove_session(login_session)
        session.pop('login_session ', None)
        session.pop('session_id ', None)
        session.pop('org_id', None)
        logger.info("Session has been deleted")
        result = {'status': "success", "message": "LOGOUT_SUCCESS"}
        return jsonify(result)
    else:
        result = {'status': "failure", "message": "LOGOUT_FAILURE"}
        return jsonify(result)