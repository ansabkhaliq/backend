import logging
import datetime
from pymysql import IntegrityError
from werkzeug.exceptions import HTTPException
from app.Resource.DatabaseBase import DatabaseBase
from app.Exception.exceptions import *


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# def exec_ok(msg="Successfully executed", data=None):
#     return {
#         'success': True,
#         'message': msg,
#         'data': data
#     }
#
#
# def exec_fail(msg="Execution failed", data=None):
#     return {
#         'success': False,
#         'message': msg,
#         'data': data
#     }


class SimpleModelResource(DatabaseBase):
    """
    A subclass of DatabaseBase, responsible for handling database
    operations regarding simple Models (customer, address, etc.)
    ** Notice **, to use this resource, the model must:
            implement the fields mapping            get_fields_mapping()
            specify the corresponding table name    get_table_name()

            please refer the Customer and the Address Model

    These operations include:
        - Insert Record
        - Update Record
        - Delete Record
        - Retrieve Record by auto increment id(pk)
        - Retrieve Record(s) by multiple fields using Model obj
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(obj):
        """
        Read field names as well as corresponding values

        :param obj: Model obj
        :return: field_value_dict -> dict
        """
        fields_mapping = obj.fields_mapping()
        obj_dict = obj.__dict__.copy()
        field_value_dict = {fields_mapping[k]: obj_dict[k] for k in obj_dict}
        return field_value_dict

    @staticmethod
    def to_model(cls, obj_dict):
        return cls(
            {cls.fields_mapping()[k]: obj_dict[k] for k in obj_dict}
        )

    def get_one_by_id(self, obj):
        """
        Retrieve on record from specific table in database

        """
        obj_type = type(obj)
        table = obj.table_name()
        query = f'SELECT * FROM {table} WHERE id=%s'
        ret = self.run_query(query, [obj.id], False)
        if ret is None:
            logger.error(f'Record not found in table {table}')
            raise NotFound(obj)
        else:
            ret_obj = obj_type(
                {obj.fields_mapping()[k]: ret[0][k] for k in ret[0]}
            )
            return ret_obj

    def get_all(self, cls):
        """return all records by the given class"""
        table = cls.table_name()
        query = f'SELECT * FROM {table}'
        obj_dict_list = self.run_query(query, [], False)
        if obj_dict_list is None:
            return []
        obj_list = []
        for ele in obj_dict_list:
            obj_list.append(cls(
                {cls.fields_mapping()[k]: ele[k] for k in ele}
            ))

        return obj_list

    # TODO batch insert
    def create(self, obj, commit=True):
        """
        Save current obj as an new instance into the database

        """
        table = obj.table_name()
        obj_dict = obj.__dict__.copy()
        del obj_dict['id']
        fields = map(
            lambda x: obj.fields_mapping()[x],
            obj_dict.keys()
        )
        fields_str = ','.join(fields)
        values = list(obj_dict.values())
        place_holders = ('%s,' * len(values))[:-1]
        query = f"INSERT into {table} ({fields_str}) VALUES ({place_holders})"
        try:
            self.run_query(query, values, commit)
            obj.id = self.cursor.lastrowid
            return obj
        except IntegrityError as e:
            logger.error(f'Create record for table {table} failed: {str(e)}')
            if e.args[0] == 1062:
                raise AlreadyExists(obj)
            if e.args[0] == 1216:
                raise ViolateFKConstraint(obj)
            else:
                raise OtherException(obj)
        except Exception as e:
            logger.error(f'Create record for table {table} failed: {str(e)}')
            raise OtherException(obj)

    def update(self, obj, commit=True):
        """
        Save current obj into database according to the id

        """
        self.get_one_by_id(obj)
        table = obj.table_name()
        obj_dict = obj.__dict__.copy()
        del obj_dict['id']
        fields = map(
            lambda x: obj.fields_mapping()[x],
            obj_dict.keys()
        )

        values = list(obj_dict.values())
        sets = ','.join([f'{field}=%s' for field in fields])
        query = f"UPDATE {table} SET {sets} WHERE id={obj.id}"
        try:
            self.run_query(query, values, commit)
        except IntegrityError as e:
            logger.error(f'Update record in table {table} failed: {str(e)}')
            if e.args[0] == 1062:
                raise AlreadyExists(obj)
            if e.args[0] == 1216:
                raise ViolateFKConstraint(obj)
            else:
                raise OtherException(obj)
        except Exception as e:
            logger.error(f'Update record in table {table} failed: {str(e)}')
            raise OtherException(obj)

    def delete(self, obj, commit=True):
        """
        Delete current obj from database according to the id

        """
        obj = self.get_one_by_id(obj)
        table = obj.table_name()
        query = f'DELETE FROM {table} WHERE id=%s'
        self.run_query(query, [obj.id], commit)

    def find_all(self, obj):
        """
        Exact match records by obj, do not support filtering Nulls.

        :param  obj
        :return exact one obj
        :raise  OtherException
        """
        table = obj.table_name()
        cls = type(obj)
        fv_dict = self.to_dict(obj)
        for k, v in list(fv_dict.items()):
            if v is None:
                del fv_dict[k]

        if len(fv_dict) == 0:
            return []

        fields = fv_dict.keys()
        values = list(fv_dict.values())

        where_clause = 'WHERE ' + ' AND '.join(
            [f'{field}=%s' for field in fields]
        )
        query = f'SELECT * FROM {table} {where_clause}'
        try:
            ret_list = self.run_query(query, values, False)
            if ret_list is None:
                return []

            obj_list = [self.to_model(cls, record) for record in ret_list]
            return obj_list

        except Exception as e:
            logger.error(f'Unexpected error while executing query: {self.cursor._last_executed}\n%s', e)
            raise OtherException(obj)

    def find_one(self, obj):
        """
        Exact match one record by obj, do not support filtering Nulls.

        :param  obj
        :return exact one obj
        :raise  MultipleRecordsFound, OtherException, NotFound
        """
        ret_list = self.find_all(obj)
        if len(ret_list) == 0:
            raise NotFound(obj)
        elif len(ret_list) > 1:
            raise MultipleRecordsFound(obj)
        else:
            return ret_list[0]
