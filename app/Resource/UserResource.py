import logging
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from .DatabaseBase import DatabaseBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class UserResource(DatabaseBase):
    """
    A subclass of DatabaseBase, responsible for handling database
    operations regarding users
    
    These operations include:
        - User authentication
        - User creation
    """

    def __init__(self):
        super().__init__()


    def validate_username_password(self, username: str, password: str) -> str:
        """
        Retrieves the customer's organisation ID and password, based on the 
        the input username, and vaidates the user's identity

        Args:
            username: taken from user input
            password: hashed password string
        """
        query = "SELECT customers_org_id, passwd FROM userinfo WHERE username=%s"
        values = [username]
        result = self.run_query(query, values, False)
        if result is not None:
            result = result[0]
            if check_password_hash(result['passwd'], password):
                logger.info("Logged in successfully")
                return result['customers_org_id']
            else:
                logger.info("Incorrect username or password entered")
                return None
        else:
            logger.info(f"Could not find user '{username}'")
            return None


    def retrieve_api_key_pw(self, org_id: str) -> Tuple[str, str]:
        """
        This method retrieves the API key and password based on the user's 
        organsisation ID

        Args:
            org_id - the organisation ID of the user
        """
        query = "SELECT api_org_key, api_org_pw FROM customers WHERE org_id=%s"
        values = [org_id]
        result = self.run_query(query, values, False)
        if result is not None:
            result = result[0]
            return result["api_org_key"], result["api_org_pw"]
        else:
            logger.error("Could not retrieve API key and password")
            return None, None


    def create_user(self, username: str, password: str):
        """
        Creates a new user in the database

        Args:
            username: username
            password: password
        """
        org_id = "11EA64D91C6E8F70A23EB6800B5BCB6D"
        hpassword = generate_password_hash(password)
        query = "INSERT INTO userinfo (customers_org_id, username, passwd) VALUES (%s,%s,%s)"
        values = [org_id, username, hpassword]
        self.run_query(query, values, True)
        logger.info(f"Successfully created new user '{username}'")
