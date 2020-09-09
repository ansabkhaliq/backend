import logging
import pymysql

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DatabaseResource:
    """
    This class represents an abstract base class for database operations.
    It is responsible for establishing a connection to the database and
    executing SQL queries.
    """

    def __init__(self):
        # Establish a connection to the database
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='squizz',
                                          db='squizz_app',
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
        if not self.connection.open :
            self.connection.ping(reconnect=True)
            logger.info("Reconnecting to the database")
        try:
            self.cursor.execute(query, values)
            if commit:
                self.connection.commit()
            return None if not self.cursor.rowcount else self.cursor.fetchall()
        except Exception as e:
            logger.error("Could not execute the query" , e)
