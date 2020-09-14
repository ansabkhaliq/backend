import logging
from .DatabaseBase import DatabaseBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SessionResource(DatabaseBase):
    """
    A subclass of DatabaseBase, responsible for handling database
    operations regarding sessions
    
    These operations include:
        - Session storage
        - Session validation
        - Session deletion
    """

    def __init__(self):
        super().__init__()

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