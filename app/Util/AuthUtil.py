import os
from flask import session
from Resource.UserResource import UserResource
from Resource.SessionResource import SessionResource
from ..Service.SquizzGatewayService import SquizzGatewayService

user_resource = UserResource()
session_resource = SessionResource()
base_url = os.environ.get('BASE_URL')

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

    if session_resource.validate_session(login_session, org_id):
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

    return SquizzGatewayService(base_url, org_id, api_org_key, api_org_pw)
