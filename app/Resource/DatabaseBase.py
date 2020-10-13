import logging
import pymysql
from pymysql import IntegrityError
from werkzeug.exceptions import HTTPException
from app import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DatabaseBase:
    """
    This class represents an abstract base class for database operations.
    It is responsible for establishing a connection to the database and
    executing SQL queries.
    """

    def __init__(self):
        # Establish a connection to the database
        self.connection = pymysql.connect(host=config.HOST,
                                          user=config.USER,
                                          password=config.PASSWORD,
                                          db=config.DB_NAME,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=True,
                                          read_timeout=None,
                                          write_timeout=None)

        self.cursor = self.connection.cursor()
        self.connection.get_autocommit()

    def run_query(self, query: str, values: list, commit: bool = False):
        """
        Runs an SQL query against the MySQL database and returns the result

        Args:
            query: a MySQL query string
            values: a list of values for the query
            commit: indicates whether to commit after execution
        """
        while not self.connection.open:
            self.connection.ping(reconnect=True)
            logger.info("Reconnecting to the database")
        try:
            self.cursor.execute(query, values)
            if commit:
                self.connection.commit()
            return None if not self.cursor.rowcount else self.cursor.fetchall()
        except Exception as e:
            logger.error("Could not execute the query", e)

    def run(self, query: str, values: list, commit: bool = False):
        """
        Better Exception handling
        Runs an SQL query against the MySQL database and returns the result

        Args:
            query: a MySQL query string
            values: a list of values for the query
            commit: indicates whether to commit after execution
        """
        while not self.connection.open:
            self.connection.ping(reconnect=True)
            logger.info("Reconnecting to the database")
        try:
            self.cursor.execute(query, values)
            if commit:
                self.connection.commit()
            return None if not self.cursor.rowcount else self.cursor.fetchall()
        except Exception as e:
            logger.error("Could not execute the query", e)
            raise e
