from app import config
from flask import session
from app.Resource.UserResource import UserResource
from app.Resource.SessionResource import SessionResource
from app.Service.SquizzGatewayService import SquizzGatewayService


# -- Helper functions
def validate_login_session(login_session=None):
    """
    Determine whether or not the current user
    has an existing session within the database

    Args:
        None
    """
    if not login_session:
        login_session = session.get('login_session')

    org_id = "11EA64D91C6E8F70A23EB6800B5BCB6D" # session.get('ord_id')

    session_resource = SessionResource()
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

    base_url = config.BASE_URL
    api_org_key = config.API_ORG_KEY
    api_org_pw = config.API_ORG_PASSWORD
    supplier_org_id = config.SUPPLIER_ORG_ID
    
    return SquizzGatewayService(base_url, 
                                org_id,
                                api_org_key,
                                api_org_pw,
                                supplier_org_id)
