
import logging
from flask import Blueprint, request, jsonify, session
from app.Util import AuthUtil as authUtil
from Resource.UserResource import UserResource
from app.Service import UserService as user_service
import app.main as main

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Configure Flask application

user = Blueprint('user', __name__)


# Initialise database resource objects
user_resource = UserResource()


@user.route('/api/login', methods=['POST'])
def login_post():
    if authUtil.validate_login_session():
        result = {'status': "success", 'data': {"session_id": session.get('login_session')}, "message": "LOGIN_EXIST"}
        return jsonify(result)

    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')

    return jsonify(user_service.validate(username,password))

@user.route('/api/logout', methods=['GET'])
def logout():
    login_session = session.get('login_session')
    if authUtil.validate_login_session():
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