import logging
from .DatabaseBase import DatabaseBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ModelMetadataResource(DatabaseBase):
    def __init__(self):
        super().__init__()

    def insert_metadata(self, product_id: str, product_code: str, meta_json_string: str) -> int:
        insert_query = (
            """INSERT into model_metadata(product_id,product_code,meta_json_string) values(%d,%s,%s) 
               """)
        values = [product_id, product_code, meta_json_string]
        try:
            self.run_query(insert_query, values, True)
        except Exception as e:
            self.connection.rollback()
            logger.error('Exception occurred when inserting order', e)
            return 0
        return 1
