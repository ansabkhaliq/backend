import logging
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from .DatabaseResource import DatabaseResource

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class UserResource(DatabaseResource):
    """
    A subclass of DatabaseResource, responsible for handling database
    operations regarding users
    
    These operations include:
        - User authentication
        - Session creation, validation, and deletion
        - User creation
    """

    def __init__(self):
        super().__init__()


    def validate_username_password(self, username: str, password: str) -> str:
        """
        Retrieves the customer's organisation ID and password, based on the 
        the inputted username, and vaidates the user's identity

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
        

    def store_session(self, login_session: str, org_id: str):
        """
        Creates a new login session within the database

        Args:
            login_session - the session string
            org_id - the orginisation ID of the user
        """
        query = "INSERT INTO session (id, customers_org_id) VALUES (%s, %s)"
        values = [login_session, org_id]
        self.run_query(query, values, True)


    def validate_session(self, login_session, org_id: str):
        """
        This method validates whether login_session exists already in the database

        Args:
            login_session - the session string
            org_id - the orginisation ID of the user
        """
        query = "SELECT count(*) as num FROM session WHERE id=%s and customers_org_id=%s"
        values = [login_session, org_id]
        result = self.run_query(query, values, False)
        if result is not None and result[0]['num'] > 0:
            return True
        else:
            logger.info("Could not find an existing session for the given user")
            return False


    def remove_session(self, login_session: str):
        """
        Deletes the login session record from the database

        Args:
            login_session: the session string
        """
        query = "DELETE FROM session WHERE id = %s"
        values = [login_session]
        self.run_query(query, values, True)
        logger.info(f"Removed session {login_session} from the database")


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
